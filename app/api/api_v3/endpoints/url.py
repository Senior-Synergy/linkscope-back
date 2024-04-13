from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import database
from app.api.api_v3 import schemas
from app.repository.crud_v3 import crud

router = APIRouter()

get_db = database.get_db


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /url!"}


@router.get("/{url_id}", response_model=schemas.UrlExtended, status_code=200)
def get_url_data_with_results(url_id: int, session: Session = Depends(get_db)):
    try:
        url = crud.retrieve_url_with_results(
            url_id, session, False)

        return url
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest/{url_id}", response_model=schemas.UrlExtended, status_code=200)
def get_url_data_with_latest_result_only(url_id: int, session: Session = Depends(get_db)):
    try:
        url = crud.retrieve_url_with_results(
            url_id, session, True)

        return url
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=list[schemas.UrlExtended], status_code=200)
def get_all_urls(session: Session = Depends(get_db)):
    try:
        urls = crud.retrieve_all_urls(session, True)

        return urls
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", status_code=200)
def get_matched_urls(request: schemas.UrlSearch, session: Session = Depends(get_db)):
    try:
        # Not necessary for now. Will implement later...
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
