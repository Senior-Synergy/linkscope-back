from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas
from app.repository import url_crud
from app.urlresult import *
from app.utils import load_model

router = APIRouter()
get_db = database.get_db


@router.post("/", status_code=status.HTTP_200_OK)
def scan_url(request: schemas.Url, db_session: Session = Depends(get_db)):
    # initialize
    url = request.url
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


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /scan!"}
