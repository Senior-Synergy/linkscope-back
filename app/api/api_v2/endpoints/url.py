from fastapi import APIRouter, Depends, status
from app import database, schemas
from sqlalchemy.orm import Session
from app.repository import url_crud
from app.urlresult import *

router = APIRouter()
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def scan_url(request: str, db: Session = Depends(get_db)):
    # First: extract url?
    return url_crud.create_ScanResult(request, db)


@router.get("/{scan_id}", response_model=schemas.ScanResult)
def get_ScanResult(scan_id: int, db: Session = Depends(get_db)):
    return url_crud.get_ScanResult(scan_id, db)


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /url!"}
