from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Result, Url, Feature
from app.api.api_v3 import schemas
from app.repository.crud_v3 import result_crud, url_crud, feature_crud, submission_crud

from app.utils import load_joblib_model
from app.urlresult import URLFeatures, URLResult

import json

router = APIRouter()

# response_model=schemas.ResultCreateResponse


@router.post("/create", status_code=200)
def create_result_route(request: schemas.ResultCreateRequest, db: Session = Depends(get_db)):
    # Submitted data
    submitted_url = request.url
    submission_id = request.submission_id

    # Extracted data
    feature = URLFeatures(submitted_url)
    result = URLResult(feature)

    model_features = feature.get_model_features()
    extra_url_info = feature.get_extra_url_info()
    extra_features = feature.get_extra_features()

    final_url = result.final_url

    # Retrieve submission object first
    submission_obj = submission_crud.get_submission(submission_id, db)

    if not submission_obj:
        print("submission_obj", submission_obj, "error............")
        return

    # Check if URL already exists in the DB. If yes, update; else, create new.
    url_obj = url_crud.retrieve_url_by_final_url(final_url, db)

    if not url_obj:
        print("url_obj OK", url_obj, "no retrieve_url_by_final_url", final_url)

    if url_obj:
        url_data = {"final_url": final_url,
                    "hostname": extra_url_info.get('hostname'),
                    "domain": extra_url_info.get('domain'),
                    "registrar": extra_url_info.get('registrar'),
                    "ip_address": extra_url_info.get('ip_address'),
                    "subdomains": json.dumps(extra_url_info.get('subdomains')),
                    "scheme": extra_url_info.get('scheme'),
                    # ----------------------------------------------------
                    "creation_date": extra_url_info.get('creation_date'),
                    "expiration_date": extra_url_info.get('expiration_date'),
                    "domainage": extra_url_info.get('domainage'),
                    "domainend": extra_url_info.get('domainend'),
                    "city": extra_url_info.get('city'),
                    "state": extra_url_info.get('state'),
                    "country": extra_url_info.get('country')}

        url_obj = url_crud.update_url(url_obj, url_data, db)
        if not url_obj:
            print("url_obj", url_obj, "error case after update")
    else:
        url_data = Url(final_url=final_url,
                       hostname=extra_url_info.get('hostname'),
                       domain=extra_url_info.get('domain'),
                       registrar=extra_url_info.get('registrar'),
                       ip_address=extra_url_info.get('ip_address'),
                       subdomains=json.dumps(extra_url_info.get('subdomains')),
                       scheme=extra_url_info.get('scheme'),
                       creation_date=extra_url_info.get(
                           'creation_date'),
                       expiration_date=extra_url_info.get(
                           'expiration_date'),
                       domainage=extra_url_info.get('domainage'),
                       domainend=extra_url_info.get('domainend'),
                       city=extra_url_info.get('city'),
                       state=extra_url_info.get('state'),
                       country=extra_url_info.get('country'),
                       google_safe_browsing=extra_url_info.get('google_safe_browsing'))
        url_obj = url_crud.create_url(url_data, db)
        if not url_obj:
            print("url_obj", url_obj, "error case after create")

    if not url_obj:
        # TODO Add error handling...
        print("url_obj", url_obj, "error............")
        return

    feature_data = Feature(domainlength=model_features.get('domainlength'),  # 1
                           www=model_features.get('www'),  # 2
                           https=model_features.get('https'),  # 3
                           short_url=model_features.get('short_url'),  # 4
                           ip=model_features.get('ip'),  # 5
                           dash_count=model_features.get('dash_count'),  # 6
                           equal_count=model_features.get('equal_count'),  # 7
                           dot_count=model_features.get('dot_count'),  # 8
                           slash_count=model_features.get('slash_count'),  # 9
                           underscore_count=model_features.get(
                               'underscore_count'),  # 10
                           digit_count=model_features.get('digit_count'),  # 11
                           pc_emptylink=model_features.get(
                               'pc_emptylink'),  # 12
                           pc_extlink=model_features.get('pc_extlink'),  # 13
                           pc_requrl=model_features.get('pc_requrl'),  # 14
                           zerolink=model_features.get('zerolink'),  # 15
                           ext_favicon=model_features.get('ext_favicon'),  # 16
                           sfh=model_features.get('sfh'),  # 17
                           redirection=model_features.get('redirection'),  # 18
                           domainend=model_features.get('domainend'),  # 19
                           # --------------------------------------------------------
                           shortten_url=extra_features.get('shortten_url'),
                           ip_in_url=extra_features.get('ip_in_url'),
                           empty_links_count=extra_features.get(
                               'empty_links_count'),
                           external_links=json.dumps(
                               extra_features.get('external_links')),
                           external_img_requrl=json.dumps(extra_features.get(
                               'external_img_requrl')),
                           external_audio_requrl=json.dumps(extra_features.get(
                               'external_audio_requrl')),
                           external_embed_requrl=json.dumps(extra_features.get(
                               'external_embed_requrl')),
                           external_iframe_requrl=json.dumps(extra_features.get(
                               'external_iframe_requrl')),
                           len_external_links=extra_features.get(
                               'len_external_links'),
                           len_external_img_requrl=extra_features.get(
                               'len_external_img_requrl'),
                           len_external_audio_requrl=extra_features.get(
                               'len_external_audio_requrl'),
                           len_external_embed_requrl=extra_features.get(
                               'len_external_embed_requrl'),
                           len_external_iframe_requrl=extra_features.get(
                               'len_external_iframe_requrl'))

    feature_obj = feature_crud.create_feature(feature_data, db)

    result_data = Result(submitted_url=submitted_url,
                         phish_prob=result.phish_prob,
                         verdict=result.verdict,
                         trust_score=result.trust_score,
                         submission=submission_obj,
                         url=url_obj,
                         feature=feature_obj)

    result_obj = result_crud.create_result(result_data, db)

    return {"result_id": result_obj.result_id}


@router.post("/create-test", status_code=200)
def create_result_test_route(url: str, db: Session = Depends(get_db)):
    # Submitted data
    submitted_url = url

    # Extracted data
    feature = URLFeatures(submitted_url)
    result = URLResult(feature)

    model_features = feature.get_model_features()
    extra_url_info = feature.get_extra_url_info()
    extra_feature = feature.get_extra_features()

    final_url = result.final_url

    url_data_dict = {
        'final_url': final_url,
        'hostname': extra_url_info.get('hostname'),
        'domain': extra_url_info.get('domain'),
        'registrar': extra_url_info.get('registrar'),
        'ip_address': extra_url_info.get('ip_address'),
        'subdomains': extra_url_info.get('subdomains'),
        'scheme': extra_url_info.get('scheme'),
        'creation_date': extra_url_info.get('creation_date'),
        'expiration_date': extra_url_info.get('expiration_date'),
        'domainage': extra_url_info.get('domainage'),
        'domainend': extra_url_info.get('domainend'),
        'city': extra_url_info.get('city'),
        'state': extra_url_info.get('state'),
        'country': extra_url_info.get('country'),
        'google_safe_browsing': extra_url_info.get('google_safe_browsing')
    }

    feature_data_dict = {
        'domainlength': model_features.get('domainlength'),
        'www': model_features.get('www'),
        'https': model_features.get('https'),
        'short_url': model_features.get('short_url'),
        'ip': model_features.get('ip'),
        'dash_count': model_features.get('dash_count'),
        'equal_count': model_features.get('equal_count'),
        'dot_count': model_features.get('dot_count'),
        'slash_count': model_features.get('slash_count'),
        'underscore_count': model_features.get('underscore_count'),
        'digit_count': model_features.get('digit_count'),
        'pc_emptylink': model_features.get('pc_emptylink'),
        'pc_extlink': model_features.get('pc_extlink'),
        'pc_requrl': model_features.get('pc_requrl'),
        'zerolink': model_features.get('zerolink'),
        'ext_favicon': model_features.get('ext_favicon'),
        'sfh': model_features.get('sfh'),
        'redirection': model_features.get('redirection'),
        'domainend': model_features.get('domainend'),
        # --------------------------------------------------------------------
        'shortten_url': extra_feature.get('shortten_url'),
        'ip_in_url': extra_feature.get('ip_in_url'),
        'empty_links_count': extra_feature.get('empty_links_count'),
        'external_links': extra_feature.get('external_img_requrl'),
        'external_img_requrl': extra_feature.get('external_img_requrl'),
        'external_audio_requrl': extra_feature.get('external_audio_requrl'),
        'external_embed_requrl': extra_feature.get('external_embed_requrl'),
        'external_iframe_requrl': extra_feature.get('external_iframe_requrl'),
        'len_external_links': extra_feature.get('len_external_img_requrl'),
        'len_external_img_requrl': extra_feature.get('len_external_img_requrl'),
        'len_external_audio_requrl': extra_feature.get('len_external_embed_requrl'),
        'len_external_embed_requrl': extra_feature.get('len_external_embed_requrl'),
        'len_external_iframe_requrl': extra_feature.get('len_external_iframe_requrl'),
    }

    result_data_dict = {
        'submitted_url': submitted_url,
        'is_phish': result.is_phish,
        'phish_prob': result.phish_prob,
        'verdict': result.verdict,
        'trust_score': result.trust_score
    }

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

    return ({"url_data": url_data_dict,
            "result_data": result_data_dict,
             "feature_data":  feature_data_dict})


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


@ router.post("/result-list/search", response_model=schemas.UrlSearchResponse, status_code=200)
def search_results_by_keyword(request: schemas.UrlSearchRequest, db: Session = Depends(get_db)):
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
