from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from app import models
from app.database import get_db

from app.api.api_v3 import schemas
from app.api.api_v3.schemas import SubmissionResponse, SubmissionCreateResponse

from app.repository.crud_v3 import url_crud, submission_crud, result_crud
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
    urls = request.urls

    # Create submission_data
    submission_data = models.Submission()

    for url in urls:
        # Get URL scan_obj
        feature = URLFeatures(url)
        result = URLResult(feature)

        final_url = result.final_url
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
                                      "hostname": extra_url_info.get('hostname'),
                                      "domain": extra_url_info.get('domain'),
                                      "registrar": extra_url_info.get('registrar'),
                                      "ip_address": extra_url_info.get('ip_address'),
                                      "subdomains": extra_url_info.get('subdomains'),
                                      "scheme": extra_url_info.get('scheme'),
                                      # extra domain infomation
                                      "creation_date": extra_url_info.get('creation_date'),
                                      "expiration_date": extra_url_info.get('expiration_date'),
                                      "domainage": extra_url_info.get('domainage'),
                                      "domainend": extra_url_info.get('domainend'),
                                      "city": extra_url_info.get('city'),
                                      "state": extra_url_info.get('state'),
                                      "country": extra_url_info.get('country'),
                                      "google_is_malicious": extra_url_info.get('google_is_malicious')})
        else:
            url_data = models.Url(final_url=final_url,
                                  hostname=extra_url_info.get('hostname'),
                                  domain=extra_url_info.get('domain'),
                                  registrar=extra_url_info.get('registrar'),
                                  ip_address=extra_url_info.get('ip_address'),
                                  subdomains=json.dumps(
                                      extra_url_info.get('subdomains')),
                                  scheme=extra_url_info.get('scheme'),
                                  # extra domain infomation
                                  creation_date=extra_url_info.get(
                                      'creation_date'),
                                  expiration_date=extra_url_info.get(
                                      'expiration_date'),
                                  domainage=extra_url_info.get('domainage'),
                                  domainend=extra_url_info.get('domainend'),
                                  city=extra_url_info.get('city'),
                                  state=extra_url_info.get('state'),
                                  country=extra_url_info.get('country'),
                                  google_is_malicious=extra_url_info.get('google_is_malicious'))
            url_to_insert.append(url_data)

        # Create feature_data and result_data ,and append to list for bulk insert
        feature_data = models.Feature(domainlength=model_features.get('domainlength'),  # 1
                                      www=model_features.get('www'),  # 2
                                      https=model_features.get('https'),  # 3
                                      short_url=model_features.get(
                                          'short_url'),  # 4
                                      ip=model_features.get('ip'),  # 5
                                      dash_count=model_features.get(
                                          'dash_count'),  # 6
                                      equal_count=model_features.get(
                                          'equal_count'),  # 7
                                      dot_count=model_features.get(
                                          'dot_count'),  # 8
                                      slash_count=model_features.get(
                                          'slash_count'),  # 9
                                      underscore_count=model_features.get(
                                          'underscore_count'),  # 10
                                      digit_count=model_features.get(
                                          'digit_count'),  # 11
                                      pc_emptylink=model_features.get(
                                          'pc_emptylink'),  # 12
                                      pc_extlink=model_features.get(
                                          'pc_extlink'),  # 13
                                      pc_requrl=model_features.get(
                                          'pc_requrl'),  # 14
                                      zerolink=model_features.get(
                                          'zerolink'),  # 15
                                      ext_favicon=model_features.get(
                                          'ext_favicon'),  # 16
                                      sfh=model_features.get('sfh'),  # 17
                                      redirection=model_features.get(
                                          'redirection'),  # 18
                                      domainend=model_features.get(
                                          'domainend'),  # 19
                                      # --------------------------------------------------------
                                      shortten_url=extra_features.get(
                                          'shortten_url'),
                                      ip_in_url=extra_features.get(
                                          'ip_in_url'),
                                      empty_links_count=extra_features.get(
                                          'empty_links_count'),
                                      external_links=json.dumps(
                                          extra_features.get('external_links')),
                                      external_img_requrl=json.dumps(
                                          extra_features.get('external_img_requrl')),
                                      external_audio_requrl=json.dumps(
                                          extra_features.get('external_audio_requrl')),
                                      external_embed_requrl=json.dumps(
                                          extra_features.get('external_embed_requrl')),
                                      external_iframe_requrl=json.dumps(
                                          extra_features.get('external_iframe_requrl')),
                                      len_external_links=extra_features.get(
                                          'len_external_links'),
                                      len_external_img_requrl=extra_features.get(
                                          'len_external_img_requrl'),
                                      len_external_audio_requrl=extra_features.get(
                                          'len_external_audio_requrl'),
                                      len_external_embed_requrl=extra_features.get(
                                          'len_external_embed_requrl'),
                                      len_external_iframe_requrl=extra_features.get('len_external_iframe_requrl'))

        result_data = models.Result(submitted_url=url,
                                    phish_prob=result.phish_prob,
                                    phish_prob_mod =result.phish_prob_mod,
                                    has_soup =result.has_soup,                                    
                                    submission=submission_data,
                                    url=url_data,
                                    feature=feature_data
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
