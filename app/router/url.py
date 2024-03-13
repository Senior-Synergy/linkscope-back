from fastapi import APIRouter, Depends, status, HTTPException
from app import database, models, schemas
from sqlalchemy.orm import Session
from app.repository import url_crud
from app.urlresult import *
#from app.models import ScanResult, ScanStatus
#from app.urlresult import *
#model = load_model("data/model_new.gzip") 

router = APIRouter(prefix="/url",
    tags=['url'])

get_db = database.get_db

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ScanResult(request: schemas.ScanResultCreate, db: Session = Depends(get_db)):
    print('hello')
    return url_crud.create_ScanResult(request, db)

@router.get("/{scan_id}", response_model=schemas.ScanResult)
def get_ScanResult(scan_id: int, db: Session = Depends(get_db)):
    return url_crud.get_ScanResult(scan_id, db)

@router.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}

'''
@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API documentation")


@router.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()

@router.get("/scan/")
async def get_result(url: str):
    # This is where the processing logic should be...
    # Idea: return scan_id != 0 if the scan is successful.
    # Then, use that scan_id to fetch data w/ result/?scan_id=...
    # For now, let's scope the mechanism to work on only single URL per request first.
    scan_status = ScanStatus(url=url, scan_id=1)

    return scan_status


@router.get("/result/")
async def get_result(scan_id: int):
    # Result fetching logic with scan_id...
    result_data = {"url": "example.com"}
    scan_result = ScanResult(scan_id=scan_id, results=result_data)

    return scan_result
'''