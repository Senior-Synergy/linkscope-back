from fastapi import APIRouter, Depends, status, HTTPException
from app import database, models, schemas
from sqlalchemy.orm import Session
from app.repository import url
from app.urlresult import *
#from app.models import ScanResult, ScanStatus
#from app.urlresult import *
#model = load_model("data/model_new.gzip") 

router = APIRouter(prefix="/url",
    tags=['URL'])

get_db = database.get_db

# create data to database
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ScanResult(request: schemas.ScanResultCreate, db: Session = Depends(get_db)):
    return url.create_ScanResult(request, db)

# get data from database and return to fontend
@router.get("/{scan_id}", response_model=schemas.ScanResult)
def get_ScanResult(scan_id: int, db: Session = Depends(get_db)):
    return url.get_ScanResult(scan_id, db)

@router.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}