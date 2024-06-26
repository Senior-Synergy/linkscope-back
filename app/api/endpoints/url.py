from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.repository import url_crud, result_crud

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello, From Backend's /url!"}


@router.get("/info/{url_id}", response_model=schemas.UrlBase, status_code=200)
def get_url_data(url_id: int, db: Session = Depends(get_db)):
    url = url_crud.retrieve_url_by_url_id(url_id, db)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    return {
        **url.__dict__,
    }


@router.post("/similar/{url_id}", response_model=list[schemas.UrlBase], status_code=200)
def get_similar_url_data(url_id: int, request: schemas.UrlSimilarUrlRequest, db: Session = Depends(get_db)):
    url = url_crud.retrieve_url_by_url_id(url_id, db)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    similar_urls = url_crud.retrieve_similar_urls(
        db, url.url_id, url.final_url, request.threshold, request.amount)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    return [url.__dict__ for url in similar_urls]


@router.post("/results/{url_id}", response_model=schemas.UrlResultPaginatedResponse, status_code=200)
def get_url_results_data_paginated(url_id: int, request: schemas.UrlResultPaginatedRequest, db: Session = Depends(get_db)):
    url = url_crud.retrieve_url_by_url_id(url_id, db)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    results = result_crud.retrieve_paginated_results_by_url_id(
        db, url_id, request.page, request.page_size, request.sort_by, request.sort_direction)

    return results


@router.get("/info-extended/{url_id}", response_model=schemas.UrlExtended, status_code=200)
def get_url_data_with_results(url_id: int, db: Session = Depends(get_db)):
    url = url_crud.retrieve_url_by_url_id(url_id, db)

    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"URL with ID '{url_id}' not found"
        )

    results = result_crud.retrieve_all_results_by_url_id(url_id, db)
    similar_urls = url_crud.retrieve_similar_urls(
        db, url.url_id, url.final_url, 10)

    return {
        **url.__dict__,
        "results": [result.__dict__ for result in results],
        "similar_urls": [url.__dict__ for url in similar_urls]
    }


@router.get("/info-extended/latest/{url_id}", response_model=schemas.Url, status_code=200)
def get_url_data_with_latest_result_only(url_id: int, db: Session = Depends(get_db)):
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


@router.get("/list/all", response_model=list[schemas.Url], status_code=200)
def get_all_urls(db: Session = Depends(get_db)):
    url_list_data = url_crud.retrieve_all_urls(db)

    urls = []

    for url in url_list_data:
        result = result_crud.retrieve_latest_result_by_url_id(url.url_id, db)

        urls.append({
            **url.__dict__,
            "result": result
        })

    return urls


@ router.post("/list/search", response_model=schemas.UrlSearchResponse, status_code=200)
def search_results_by_keyword(request: schemas.UrlSearchRequest, db: Session = Depends(get_db)):
    search_results = url_crud.retrieve_filtered_paginated_urls(
        db,
        request.keyword,
        request.page,
        request.page_size,
        request.creation_date_start,
        request.creation_date_end,
        request.phish_prob_min,
        request.phish_prob_max,
        request.country,
        request.sort_by,
        request.sort_direction,
    )

    return search_results
