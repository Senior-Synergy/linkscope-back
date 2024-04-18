from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy import update, asc, desc, and_, or_

from typing import Optional
from math import ceil

from app.models import Url, Feature, Result, Submission
from fastapi import HTTPException
from app.urlresult import *


def retrieve_url_with_results(url_id: int, session: Session, latest: bool):
    try:
        url = session.query(Url).filter(Url.url_id == url_id).first()

        if not url:
            raise HTTPException(status_code=404, detail="URL not found")

        if not latest:
            results = session.query(Result).filter(Result.url_id == url_id).order_by(
                desc(Result.datetime_created)).all()

            return {
                **url.__dict__,
                "results": [result for result in results]
            }
        else:
            result = session.query(Result).filter(Result.url_id == url_id).order_by(
                desc(Result.datetime_created)).first()

            return {
                **url.__dict__,
                "result": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_all_urls(session: Session):
    try:
        url_data = session.query(Url).all()

        urls = []

        for url in url_data:
            result = session.query(Result).\
                filter(Result.url_id == url.url_id).\
                order_by(desc(Result.datetime_created)).\
                first()

            urls.append({
                **url.__dict__,
                "result": result
            })

        return urls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_urls(
    session: Session,
    keyword: str,
    page: int,
    page_size: int,
    creation_date_start: Optional[datetime] = None,
    creation_date_end: Optional[datetime] = None,
    phish_prob_min: Optional[float] = None,
    phish_prob_max: Optional[float] = None,
    country: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = 'desc'
):
    try:
        offset = (page - 1) * page_size
        query = session.query(Result, Url).join(
            Url, Result.url_id == Url.url_id)

        query = query.filter(or_(Url.final_url.ilike(
            f"%{keyword}%"), Result.submitted_url.ilike(f"%{keyword}%")))

        # Additional filters on results
        if creation_date_start:
            query = query.filter(
                Result.datetime_created >= creation_date_start)
        if creation_date_end:
            query = query.filter(Result.datetime_created <= creation_date_end)
        if phish_prob_min:
            query = query.filter(Result.phish_prob >= phish_prob_min)
        if phish_prob_max:
            query = query.filter(Result.phish_prob <= phish_prob_max)

        # Additional filters on urls
        if country:
            query = query.filter(Url.country == country)

        # Sorting
        if sort_by:
            if sort_by in Url.__table__.columns.keys():
                if sort_direction == 'asc':
                    query = query.order_by(asc(getattr(Url, sort_by)))
                elif sort_direction == 'desc':
                    query = query.order_by(desc(getattr(Url, sort_by)))
            elif sort_by in Result.__table__.columns.keys():
                if sort_direction == 'asc':
                    query = query.order_by(asc(getattr(Result, sort_by)))
                elif sort_direction == 'desc':
                    query = query.order_by(desc(getattr(Result, sort_by)))
            else:
                raise ValueError(f"Invalid sort column '{sort_by}'")

        total_count = query.count()
        total_pages = ceil(total_count / page_size)

        fetched_data = query.offset(offset).limit(page_size).all()

        # Convert fetched data into a list of dictionaries
        formatted_data = []

        for result, url in fetched_data:
            formatted_data.append({
                **result.__dict__,
                "url": {
                    **url.__dict__,
                }
                # Add other attributes as needed
            })

        # formatted_data = {}
        # for url, result in fetched_data:
        #     url_dict = url.__dict__
        #     result_dict = result.__dict__
        #     url_id = url_dict['url_id']

        #     if url_id not in formatted_data:
        #         formatted_data[url_id] = {
        #             **url_dict,
        #             "results": [result_dict]
        #         }
        #     else:
        #         formatted_data[url_id]["results"].append(result_dict)

        return {"total_count": total_count, "results": formatted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_url_results(session: Session, url_id: int, latest_only: bool):
    try:
        results = []
        results_query = session.query(Result).\
            filter(Result.url_id == url_id).\
            order_by(desc(Result.datetime_created))

        if latest_only:
            results = results_query.first()
        else:
            results = results_query.all()

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_features(session: Session, feature_id: int):
    try:
        feature_data = session.query(Feature).filter(
            Feature.feature_id == feature_id).first()
        return feature_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_result_with_features(result_id: int, session: Session):
    try:
        result_data = session.query(Result).filter(
            Result.result_id == result_id).first()

        feature_data = session.query(Feature).filter(
            Feature.feature_id == result_data.feature_id).first()

        url_data = session.query(Url).\
            filter(Url.url_id == result_data.url_id).\
            first()

        return {
            **result_data.__dict__,
            "url": url_data,
            "feature": feature_data.__dict__
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_result_data_with_submission_id(submission_id: int, session: Session):
    try:
        query_result = session.query(Result).filter(
            Result.submission_id == submission_id).all()

        if not query_result:
            raise HTTPException(
                status_code=404, detail="RESULT with 'result_id: {result_id}' not found")

        results = []

        for result in query_result:
            feature_data = session.query(Feature).\
                filter(Feature.feature_id == result.feature_id).\
                first()

            url_data = session.query(Url).\
                filter(Url.url_id == result.url_id).\
                first()

            results.append({
                **result.__dict__,
                "url": url_data,
                "feature": feature_data
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_submission_data(submission_id: int, session: Session):
    try:
        # query = session.query(Submission, Result).\
        #     join(Result, Submission.submission_id == Result.submission_id).\
        #     filter(Submission.submission_id == submission_id)

        query_submission = session.query(Submission,).\
            filter(Submission.submission_id == submission_id)

        results = query_submission.first()

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
