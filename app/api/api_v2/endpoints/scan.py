from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas, models
from app.repository import url_crud
from app.urlresult import *
from app.utils import load_model

router = APIRouter()
get_db = database.get_db

'''
@router.post("/", status_code=status.HTTP_200_OK)
def scan_url(request: schemas.Url_submission, db_session: Session = Depends(get_db)):
    # initialize
    url = request.urls[0]
    model = load_model("data/model_compressed.gzip")
    result = URLresult(url, model)
    final_url = result.get_final_url()
    
    # check if URL (with final_url) is already in the DB.
    existing_scan_result = url_crud.search_url(final_url, db_session)
    
    # note: should we update if phish prob is different?
    
    if existing_scan_result:
        return existing_scan_result.scan_id
    else:
         # create new url entry in DB
        new_scan_result = url_crud.create_ScanResult(
            url, result, db_session)  
     
        if new_scan_result:
            return new_scan_result.scan_id
        else:
            return 0
'''
@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /scan!"}

#------------------- Scan and Bulk Insert all data to DB (faster) ----------------------------------------
@router.post("/list2", status_code=status.HTTP_200_OK)
def scan_all_ver2(request: schemas.Url_submission_list, db_session: Session = Depends(get_db)):
    
    # List of Data to be inserted
    url_objects = []
    feature_objects = []
    result_objects = []
    urls = request.urls
    submission_data = models.Submission()
    model = load_model("data/model_compressed.gzip")

    for i,url in enumerate(urls):
        # Get URL result
        result = URLresult(url, model)
        features_arr = result.features_arr
        # append to list
        print(f'Inserting {url} to db')
        url_objects.append(models.Url(final_url=result.get_final_url(),
                                      extra_features= result.get_extra_features(),
                                      whois_features= result.get_whois_features()))         
        feature_objects.append(models.Feature(domainlength = features_arr[0][0], #1
                                www = features_arr[0][1], # 2
                                subdomain = features_arr[0][2] , # 3
                                https = features_arr[0][3] , # 4
                                http = features_arr[0][4] , # 5
                                short_url = features_arr[0][5] , # 6
                                ip = features_arr[0][6] , # 7
                                at_count = features_arr[0][7], # 8
                                dash_count = features_arr[0][8] , # 9
                                equal_count = features_arr[0][9] , # 10
                                dot_count = features_arr[0][10] , # 11
                                underscore_count = features_arr[0][11] , # 12
                                slash_count = features_arr[0][12] , # 13
                                digit_count= features_arr[0][13] , # 14
                                log_contain = features_arr[0][14] , # 15
                                pay_contain = features_arr[0][15], # 16
                                web_contain = features_arr[0][16], #17
                                cmd_contain = features_arr[0][17], # 18
                                account_contain= features_arr[0][18], # 19
                                pc_emptylink = features_arr[0][19] , # 20
                                pc_extlink = features_arr[0][20], # 21
                                pc_requrl= features_arr[0][21] , # 22
                                zerolink = features_arr[0][22] , # 23
                                ext_favicon = features_arr[0][23], # 24
                                submit_to_email = features_arr[0][24] , # 25
                                sfh = features_arr[0][25] , # 26
                                redirection = features_arr[0][26], # 27
                                domainage = features_arr[0][27] , # 28
                                domainend = features_arr[0][28] )) # 29)
        result_objects.append(models.Result(submitted_url = url,
                                phish_prob= result.get_phish_prob(),
                                is_phishing= result.get_isPhish(),
                                submission = submission_data,
                                url = url_objects[i],
                                feature = feature_objects[i]))
    
    submission_id = url_crud.create_all_result(submission_data, url_objects, feature_objects, result_objects, db_session)   
    
    return submission_id