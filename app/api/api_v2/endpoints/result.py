from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import database, schemas
from app.repository import url_crud
from fastapi import HTTPException, status
from typing import List

router = APIRouter()
get_db = database.get_db


@router.get("/{url_id}", response_model=schemas.ScanResult, status_code=status.HTTP_200_OK)
def get_result(url_id: int, db_session: Session = Depends(get_db)):
    scan_result = url_crud.get_ScanResult(url_id, db_session)

    return scan_result


@router.post("/list", response_model=list[schemas.ScanResult], status_code=status.HTTP_200_OK)
def get_result_list(url_id_list: list[int], db_session: Session = Depends(get_db)):
    scan_result_list = []

    for url_id in url_id_list:
        scan_result = url_crud.get_ScanResult(url_id, db_session)
        scan_result_list.append(scan_result)

    return scan_result_list

# GET all URL Results
@router.get("/{scan_id}", status_code=status.HTTP_200_OK)
def get_result_by_scanid(scan_id : str, db_session: Session = Depends(get_db)):
    try:
        url_results = url_crud.get_ReportResult(scan_id, db_session)
    except Exception as e:
        print(f'Error is {str(e)}')
    if not url_results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No url_results found for scan_id {scan_id}")
    return url_results
    

@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /result!"}
