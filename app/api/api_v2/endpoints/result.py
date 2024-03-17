from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import database, schemas
from app.repository import url_crud
from fastapi import HTTPException, status
from typing import List

router = APIRouter()
get_db = database.get_db

@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /result!"}


@router.get("/list/{submission_id}",response_model=List[schemas.Url_Result], status_code=status.HTTP_200_OK)
def get_all(submission_id :int, db_session: Session = Depends(get_db)):
    try:
        url_results = url_crud.get_url_data_by_submission_id(submission_id, db_session)
    except Exception as e:
        print(f'Error is {str(e)}')
    return url_results
    


'''
@router.get("/{url_id}", response_model=schemas.Url_Result, status_code=status.HTTP_200_OK)
def get_single_url_result(url_id: int, db_session: Session = Depends(get_db)):
    scan_result = url_crud.get_url_result_by_url_id(url_id, db_session)

    return scan_result

@router.post("/list", response_model=List[schemas.Url_Result], status_code=status.HTTP_200_OK)
def get_result_list(url_id_list: list[int], db_session: Session = Depends(get_db)):
    scan_result_list = []

    for url_id in url_id_list:
        scan_result = url_crud.get_Url_Result(url_id, db_session)
        scan_result_list.append(scan_result)

    return scan_result_list
'''






