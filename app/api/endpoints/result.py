from math import e
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Result, Url, Feature
from app import schemas
from app.repository import result_crud, url_crud, feature_crud, submission_crud

from app.urlresult import URLFeatures, URLResult


router = APIRouter()


@router.post("/create", status_code=200)
def create_result_route(request: schemas.ResultCreateRequest, db: Session = Depends(get_db)):
    # Submitted data
    submitted_url = request.url
    submission_id = request.submission_id

    # Extraction and Evaluation
    feature = URLFeatures(submitted_url)
    result = URLResult(feature)

    # Data to insert
    result_data = result.get_results()
    model_features = feature.get_model_features()
    extra_url_info = feature.get_extra_url_info()
    extra_features = feature.get_extra_features()
    final_url = result.final_url

    # Retrieve submission object first
    try:
        submission_obj = submission_crud.get_submission(submission_id, db)

        if submission_obj is None:
            raise HTTPException(
                status_code=404, detail=f"Submission with submission_id: {submission_id} not found.")
    except:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch Submission with submission_id: {submission_id}.")

    # Check if URL already exists in the DB. If yes, update; else, create new.
    url_obj = url_crud.retrieve_url_by_final_url(final_url, db)

    if url_obj:
        url_data = {"final_url": final_url, **extra_url_info}
        try:
            url_obj = url_crud.update_url(url_obj, url_data, db)
        except:
            raise HTTPException(
                status_code=404, detail=f"Failed to update existing URL.")
    else:
        url_data = Url(final_url=final_url, **extra_url_info)
        try:
            url_obj = url_crud.create_url(url_data, db)
        except:
            raise HTTPException(
                status_code=500, detail=f"Failed to create new URL entry.")

    feature_data = Feature(**model_features, **extra_features)

    try:
        feature_obj = feature_crud.create_feature(feature_data, db)
    except:
        raise HTTPException(
            status_code=500, detail=f"Failed to create new Feature entry.")

    result_data = Result(submitted_url=submitted_url,
                         submission=submission_obj,
                         url=url_obj,
                         feature=feature_obj,
                         **result_data
                         )

    try:
        result_obj = result_crud.create_result(result_data, db)
    except:
        raise HTTPException(
            status_code=500, detail=f"Failed to create new Result entry.")

    return {"result_id": result_obj.result_id}


@router.post("/create-test", status_code=200)
def create_result_test_route(url: str):
    # Submitted data
    submitted_url = url

    # Extracted data
    feature = URLFeatures(submitted_url)
    result = URLResult(feature)

    result_data = result.get_results()
    model_features = feature.get_model_features()
    extra_url_info = feature.get_extra_url_info()
    extra_features = feature.get_extra_features()

    final_url = result.final_url

    # --------------------------- FOR DEBUGGING ---------------------------
    # print("url_data_dict")
    # for key, value in url_data_dict.items():
    #     print(f"Key: {key}, Value: {value}, Data Type: {type(value)}")

    # print("result_data_dict")
    # for key, value in result_data_dict.items():
    #     print(f"Key: {key}, Value: {value}, Data Type: {type(value)}")

    # print("feature_data_dict")
    # for key, value in feature_data_dict.items():
    #     print(f"Key: {key}, Value: {value}, Data Type: {type(value)}")
    # ---------------------------------------------------------------------

    return ({"final_url": final_url,
             "url_data": extra_url_info,
             "result_data": result_data,
             "model_features":  model_features,
             "extra_features":  extra_features})


@ router.get("/{result_id}", response_model=schemas.ResultExtended, status_code=200)
def get_result_with_complete_data(result_id: int, db: Session = Depends(get_db)):
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


@ router.post("/result-list/search", response_model=schemas.ResultSearchResponse, status_code=200)
def search_results_by_keyword(request: schemas.ResultSearchRequest, db: Session = Depends(get_db)):
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
