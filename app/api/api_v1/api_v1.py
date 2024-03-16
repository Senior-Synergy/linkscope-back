from fastapi import APIRouter, Depends, status, HTTPException
from app import database, models, schemas
from sqlalchemy.orm import Session
from app.repository import url
from app.urlresult import *
from app.utils import load_model
#from app.models import Url_Result, ScanStatus
#from app.urlresult import *
#model = load_model("data/model_new.gzip") 

router = APIRouter(prefix="/url",
    tags=['URL'])

get_db = database.get_db
'''
# create data to database
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_urlresult(request: schemas.Url, db: Session = Depends(get_db)):
    
    model = load_model("data/model_compressed.gzip")
    result = URLresult(request.url, model) # result from model
    final_url = result.get_final_url() 
    
    # check if URL (with final_url) is already in the DB.
    scan_result = url.get_Url_Result(final_url, db)

    if scan_result:
        return scan_result.report_id 
    else:
        # create new url entry in both DB
        url.create_Url_Result(request.url, db)
        url.create_ReportResult(request.url, db)
        return "Insert Successfully"

# get data from database and return to fontend
@router.get("/{report_id}", response_model=schemas.Url_Result)
def get_report_by_reportid(report_id: int, db: Session = Depends(get_db)):
    report_result =  url.get_Url_Result(report_id, db)
    return report_result
'''
@router.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}