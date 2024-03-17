from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas
from app.repository import url_crud
from app.urlresult import *
from app.utils import load_model

router = APIRouter()
get_db = database.get_db

'''
@router.post("/", status_code=status.HTTP_200_OK)
def scan_url(request: schemas.Url, db_session: Session = Depends(get_db)):
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

#-------------------Insert all data to DB--------------------------------------------
@router.post("/list", status_code=status.HTTP_200_OK)
def scan_all(request: schemas.Url_List, db_session: Session = Depends(get_db)):
   
     # Insert to url_submission table
    report_results = url_crud.create_url_submission(db_session)
    
    scan_id = report_results.scan_id # Get scan_id
    #print(f'scan_id is {scan_id}') 
    urls = request.urls
    model = load_model("data/model_compressed.gzip")
    #scan_id = report_results.scan_id
    for url in urls:
        # Get final_url
        result = URLresult(url, model)
        final_url = result.get_final_url()
               
        # Search whether to insert ot not
        existing_scan_result = url_crud.search_url(final_url, db_session)
       
        if not existing_scan_result:
            # Insert to url_result table
            print(f'Start Inserting {url}...')
            url_result = url_crud.create_url_result(url, scan_id, result, db_session) # insert to url_result table
            feature_result = url_crud.create_url_features(url_result.url_id, final_url, result , db_session) # insert to url_features table
        else:
            print(f'Already have {url} with url_id : {existing_scan_result.url_id} inserted in url_results table')
                   
    return report_results.scan_id
