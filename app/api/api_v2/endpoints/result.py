from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import database, schemas
from app.repository import url

router = APIRouter()
get_db = database.get_db


@router.get("/{scan_id}", response_model=schemas.ScanResult, status_code=status.HTTP_200_OK)
def get_result(scan_id: int, db_session: Session = Depends(get_db)):
    scan_result = url.get_ScanResult(scan_id, db_session)

    return scan_result


@router.post("/list", response_model=list[schemas.ScanResult], status_code=status.HTTP_200_OK)
def get_result(scan_id_list: list[int], db_session: Session = Depends(get_db)):
    scan_result_list = []

    for scan_id in scan_id_list:
        scan_result = url.get_ScanResult(scan_id, db_session)
        scan_result_list.append(scan_result)

    return scan_result_list


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /result!"}
