from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.api_v3 import schemas
from app.repository.crud_v3 import result_crud, url_crud, feature_crud

router = APIRouter()


@router.get("/{result_id}", response_model=schemas.ResultExtended, status_code=200)
async def get_result_with_complete_data(result_id: int, db: Session = Depends(get_db)):
    result_data = result_crud.retrieve_result(
        result_id, db)

    if not result_data:
        raise HTTPException(
            status_code=404, detail=f"Result with result_id: {result_id} not found")

    url_data = url_crud.retrieve_url_by_url_id(
        result_data.url_id, db)

    if not url_data:
        raise HTTPException(
            status_code=404, detail=f"URL associated with result_id: {result_id} not found")

    feature_data = feature_crud.retrieve_feature(result_data.feature_id, db)

    if not feature_data:
        raise HTTPException(
            status_code=404, detail=f"Feature associated with result_id: {result_id} not found")

    return {
        **result_data.__dict__,
        "url": url_data.__dict__,
        "feature": feature_data.__dict__ if feature_data else None
    }


@router.post("/result-list/search", response_model=schemas.UrlSearchResponse, status_code=200)
async def search_results_by_keyword(request: schemas.UrlSearchRequest, db: Session = Depends(get_db)):
    search_results = result_crud.retrieve_filtered_paginated_results(
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
