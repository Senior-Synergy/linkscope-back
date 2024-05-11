from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from app import models
from app.database import get_db

from app import schemas
from app.schemas import SubmissionResponse, SubmissionCreateResponse

from app.repository import url_crud, submission_crud, result_crud
from app.urlresult import *
from app.utils import load_model, load_joblib_model

router = APIRouter()


@router.get("/create", response_model=SubmissionCreateResponse, status_code=200)
def create_submission_route(db: Session = Depends(get_db)):
    # create new submission
    submission_id = submission_crud.create_submission(db)

    return {"submission_id": submission_id}


@router.post("/create/bulk", response_model=SubmissionResponse, status_code=200)
def create_submission_result_in_bulk_route(request: schemas.SubmissionRequest, db: Session = Depends(get_db)):

    url_to_insert, feature_to_insert, result_to_insert, url_obj_to_update = [], [], [], []
    submitted_urls = request.urls

    # Create submission_data
    submission_data = models.Submission()

    for submitted_url in submitted_urls:
        # Get URL scan_obj
        feature = URLFeatures(submitted_url)
        result = URLResult(feature)

        final_url = result.final_url
        result_data = result.get_results()
        model_features = feature.get_model_features()
        extra_url_info = feature.get_extra_url_info()
        extra_features = feature.get_extra_features()

        # Create url_data and append to list for bulk insert/update
        # Search if there is final_url in db, if exists => update, else => insert
        existing_url_result = url_crud.retrieve_url_by_final_url(final_url, db)

        if existing_url_result:
            url_data = existing_url_result
            url_obj_to_update.append({"url_id": existing_url_result.url_id,
                                      "final_url": final_url,
                                      **extra_url_info})
        else:
            url_data = models.Url(final_url=final_url, **extra_url_info)
            url_to_insert.append(url_data)

        # Create feature_data and result_data ,and append to list for bulk insert
        feature_data = models.Feature(**model_features, **extra_features)

        result_data = models.Result(submitted_url=submitted_url,
                                    submission=submission_data,
                                    url=url_data,
                                    feature=feature_data,
                                    **result_data
                                    )

        feature_to_insert.append(feature_data)
        result_to_insert.append(result_data)

    # ------------------------------End loop -----------------------------------------

    # Check if url_obj_to_update is not an empty list
    if url_obj_to_update:
        url_crud.update_url_bulk(url_obj_to_update, db)

    # Bulk insert
    submission_obj = submission_crud.create_submission_bulk(
        submission_data, url_to_insert, feature_to_insert, result_to_insert, db)

    return {"submission_id": submission_obj.submission_id}


@router.get("/retrieve/{submission_id}", response_model=schemas.Submission, status_code=200)
def get_submission_result(submission_id: int, db: Session = Depends(get_db)):
    submission_data = submission_crud.retrieve_submission_info(
        submission_id, db)

    if not submission_data:
        raise HTTPException(
            status_code=404, detail=f"Submission with submission_id: {submission_id} not found")

    result_list_data = result_crud.retrieve_results_by_submission_id(
        submission_id, db)

    if not result_list_data:
        raise HTTPException(
            status_code=404, detail=f"Result associated with submission_id: {submission_id} not found")

    results = []

    for result in result_list_data:
        url_data = url_crud.retrieve_url_by_url_id(
            result.url_id, db)

        if not url_data:
            raise HTTPException(
                status_code=404, detail=f"URL associated with result_id: {result.result_id} not found")

        results.append({
            **result.__dict__,
            "url": url_data
        })

    return {
        **submission_data.__dict__,
        "results": results,
    }
