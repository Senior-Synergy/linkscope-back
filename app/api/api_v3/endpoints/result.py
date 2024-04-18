from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.api_v3 import schemas
from app.repository.crud_v3 import crud

router = APIRouter()


@router.get("/{result_id}", response_model=schemas.ResultExtended, status_code=200)
async def get_result_with_complete_data(result_id: int, db: Session = Depends(get_db)):
    try:
        result = crud.retrieve_result_with_features(
            result_id, db)

        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/result-list/search", response_model=schemas.UrlSearchResponse, status_code=200)
async def search_results_by_keyword(request: schemas.UrlSearchRequest, db: Session = Depends(get_db)):
    try:
        search_results = crud.retrieve_urls(
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
