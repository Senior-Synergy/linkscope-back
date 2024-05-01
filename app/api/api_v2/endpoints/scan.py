from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas, models
from app.repository import url_crud
from app.urlresult import *
from app.utils import load_model

router = APIRouter()
get_db = database.get_db


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /scan!"}

# Scan and Bulk Insert all data to DB (faster)
@router.post("/list", status_code=status.HTTP_200_OK)
def scan_all_ver2(request: schemas.Url_submission_list, db_session: Session = Depends(get_db)):
 
    url_to_insert, feature_to_insert, result_to_insert, url_obj_to_update = [], [], [], []
    urls = request.urls   
    model = load_model("data/model_compressed.gzip")
    # Create submission_data
    submission_data = models.Submission()

    for url in urls:
        # Get URL scan_obj
        scan_obj = URLResult(url, model)
        final_url= scan_obj.get_final_url()
        model_features = scan_obj.model_features
        extra_url_info = scan_obj.extra_info

        # Create url_data and append to list for bulk insert/update      
        # Search if there is final_url in db, if exists => update, else => insert
        existing_url_result = url_crud.search_url(final_url, db_session)
        if existing_url_result:             
            url_data = existing_url_result
            url_obj_to_update.append({"url_id" : existing_url_result.url_id,
                            "final_url" : final_url,
                            "hostname" : extra_url_info.get('hostname'),        
                            "domain" : extra_url_info.get('domain'),
                            "registrar" : extra_url_info.get('registrar'),
                            "ip_address" : extra_url_info.get('ip_address'),
                            "subdomains" : extra_url_info.get('subdomains'),
                            "scheme" : extra_url_info.get('scheme'),
                                # extra domain infomation
                            "creation_date" : extra_url_info.get('creation_date'),
                            "expiration_date" : extra_url_info.get('expiration_date'),            
                            "domainage" : extra_url_info.get('domainage'),
                            "domainend" : extra_url_info.get('domainend'),
                            "city" : extra_url_info.get('city'), 
                            "state" : extra_url_info.get('state'),
                            "country" :extra_url_info.get('country'),
                            "google_safe_browsing" : extra_url_info.get('google_safe_browsing')})
        else:
            url_data = models.Url(final_url= final_url,
                            hostname = extra_url_info.get('hostname'),        
                            domain = extra_url_info.get('domain'),
                            registrar = extra_url_info.get('registrar'),
                            ip_address = extra_url_info.get('ip_address'),
                            subdomains = extra_url_info.get('subdomains'),
                            scheme = extra_url_info.get('scheme'),
                                # extra domain infomation
                            creation_date = extra_url_info.get('creation_date'),
                            expiration_date = extra_url_info.get('expiration_date'),            
                            domainage = extra_url_info.get('domainage'),
                            domainend = extra_url_info.get('domainend'),
                            city = extra_url_info.get('city'), 
                            state = extra_url_info.get('state'),
                            country =extra_url_info.get('country'),
                            google_safe_browsing = extra_url_info.get('google_safe_browsing'))
            url_to_insert.append(url_data)

        # Create feature_data and result_data ,and append to list for bulk insert
        feature_data = models.Feature(domainlength = model_features.get('domainlength'), #1
                                www = model_features.get('www'), #2                                
                                https = model_features.get('https') , # 3                                
                                short_url = model_features.get('short_url') , #4
                                ip = model_features.get('ip') , #5                               
                                dash_count = model_features.get('dash_count') , #6
                                equal_count = model_features.get('equal_count') , #7
                                dot_count = model_features.get('dot_count') , #8                                
                                slash_count = model_features.get('slash_count') , #9
                                underscore_count = model_features.get('underscore_count') , #10
                                digit_count= model_features.get('digit_count') , #11                                
                                pc_emptylink = model_features.get('pc_emptylink') , #12
                                pc_extlink = model_features.get('pc_extlink'), #13
                                pc_requrl = model_features.get('pc_requrl') , #14
                                zerolink = model_features.get('zerolink') , #15
                                ext_favicon = model_features.get('ext_favicon'), #16                               
                                sfh = model_features.get('sfh') , #17
                                redirection = model_features.get('redirection'), #18                               
                                domainend = model_features.get('domainend') , #19

                                shortten_url = model_features.get('shortten_url'),
                                ip_in_url  = model_features.get('ip_in_url'),              
                                len_empty_links = model_features.get('len_empty_links'),
                                external_links  = model_features.get('external_links'),
                                len_external_links  = model_features.get('len_external_links'),
                                external_img_requrl = model_features.get('external_img_requrl'),  
                                external_audio_requrl = model_features.get('external_audio_requrl'),  
                                external_embed_requrl = model_features.get('external_embed_requrl'), 
                                external_iframe_requrl = model_features.get('external_iframe_requrl'), 
                                len_external_img_requrl = model_features.get('len_external_img_requrl'),
                                len_external_audio_requrl = model_features.get('len_external_audio_requrl'),
                                len_external_embed_requrl = model_features.get('len_external_embed_requrl'),
                                len_external_iframe_requrl = model_features.get('len_external_iframe_requrl')                                                       
                                )   
        result_data = models.Result(submitted_url = url,
                            phish_prob= scan_obj.get_phish_prob(),
                            #is_phishing= scan_obj.get_isPhish(),
                            submission = submission_data,
                            url = url_data,
                            feature = feature_data
                            )
        feature_to_insert.append(feature_data)
        result_to_insert.append(result_data)
    #--------------------- ---------End loop -----------------------------------------
    
    # Check if url_obj_to_update is not an empty list
    if url_obj_to_update:            
        url_crud.update_url_db(url_obj_to_update, db_session)
    
    # Bulk insert
    url_crud.create_all_result(submission_data, url_to_insert, feature_to_insert, result_to_insert, db_session)   
    
    return submission_data.submission_id

'''
@router.post("/", status_code=status.HTTP_200_OK)
def scan_url(request: schemas.Url_submission, db_session: Session = Depends(get_db)):
    # initialize
    url = request.urls[0]
    model = load_model("data/model_compressed.gzip")
    result_obj = URLresult(url, model)
    final_url = result_obj.get_final_url()
    
    # check if URL (with final_url) is already in the DB.
    existing_scan_result = url_crud.search_url(final_url, db_session)
    
    # note: should we update if phish prob is different?
    
    if existing_scan_result:
        return existing_scan_result.scan_id
    else:
         # create new url entry in DB
        new_scan_result = url_crud.create_ScanResult(
            url, result_obj, db_session)  
     
        if new_scan_result:
            return new_scan_result.scan_id
        else:
            return 0
'''