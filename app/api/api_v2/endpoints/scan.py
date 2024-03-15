from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas
from app.repository import url
from app.urlresult import *
from app.utils import load_model

router = APIRouter()
get_db = database.get_db


@router.post("/", status_code=status.HTTP_200_OK)
def scan_url(request: schemas.Url, db_session: Session = Depends(get_db)):
    # initialize
    model = load_model("data/model_compressed.gzip")
    result = URLresult(request.url, model)
    final_url = result.get_final_url()

    # check if URL (with final_url) is already in the DB.
    scan_result = url.get_ScanResult(final_url, db_session)

    # note: should we update if phish prob is different?

    if scan_result:
        return scan_result.scan_id
    else:
        # create new url entry in DB
        new_scan_result = url.create_ScanResult(final_url, db_session)
        if new_scan_result:
            return new_scan_result.scan_id
        else:
            return 0


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /scan!"}
