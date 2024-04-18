from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.api_v3 import schemas
from app.repository.crud_v3 import crud

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Hello, From Backend's /url!"}


@router.get("/url-info/{url_id}", response_model=schemas.UrlExtended, status_code=200)
async def get_url_data_with_results(url_id: int, db: Session = Depends(get_db)):
    try:
        url = crud.retrieve_url_with_results(
            url_id, db, False)

        return url
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/url-info/latest/{url_id}", response_model=schemas.Url, status_code=200)
async def get_url_data_with_latest_result_only(url_id: int, db: Session = Depends(get_db)):
    try:
        url = crud.retrieve_url_with_results(
            url_id, db, True)

        return url
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/url-list", response_model=list[schemas.Url], status_code=200)
async def get_all_urls(db: Session = Depends(get_db)):
    # TO-DO: Pagination
    try:
        urls = crud.retrieve_all_urls(db)
        return urls
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
