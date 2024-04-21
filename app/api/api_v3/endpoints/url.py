from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.api_v3 import schemas
from app.repository.crud_v3 import url_crud, result_crud

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Hello, From Backend's /url!"}


@router.get("/url-info/{url_id}", response_model=schemas.UrlExtended, status_code=200)
async def get_url_data_with_results(url_id: int, db: Session = Depends(get_db)):
    url = url_crud.retrieve_url_by_url_id(url_id, db)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    results = result_crud.retrieve_all_results_by_url_id(url_id, db)
    similar_urls = url_crud.retrieve_similar_urls(
        db, url.url_id, url.final_url)

    return {
        **url.__dict__,
        "results": [result.__dict__ for result in results],
        "similar_urls": [url.__dict__ for url in similar_urls]
    }


@router.get("/url-info/latest/{url_id}", response_model=schemas.Url, status_code=200)
async def get_url_data_with_latest_result_only(url_id: int, db: Session = Depends(get_db)):
    url = url_crud.retrieve_url_by_url_id(url_id, db)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    result = result_crud.retrieve_latest_result_by_url_id(url_id, db)

    return {
        **url.__dict__,
        "result": result.__dict__ if result else None,
    }


@router.get("/all", response_model=list[schemas.Url], status_code=200)
async def get_all_urls(db: Session = Depends(get_db)):
    url_list_data = url_crud.retrieve_all_urls(db)

    urls = []

    for url in url_list_data:
        result = result_crud.retrieve_latest_result_by_url_id(url.url_id, db)

        urls.append({
            **url.__dict__,
            "result": result
        })

    return urls
