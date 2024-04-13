from sqlalchemy.orm import Session
from sqlalchemy import update, desc
from app.models import Url, Feature, Result, Submission
from fastapi import HTTPException, status
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
                "results": [result]
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
                "results": [result]
            })

        return urls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_result_with_features(result_id: int, session: Session):
    try:
        result_data = session.query(Result).filter(
            Result.result_id == result_id).first()

        if not result_data:
            raise HTTPException(
                status_code=404, detail="RESULT with 'result_id: {result_id}' not found")

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
