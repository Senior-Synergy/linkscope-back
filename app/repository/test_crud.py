from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, and_, or_
from Levenshtein import distance
from datetime import datetime

from typing import Optional

from app.models import Url, Feature, Result, Submission
from fastapi import HTTPException, status


def retrieve_url_extended(url_id: int, session: Session, latest: bool, threshold: int = 5):
    try:
        url = session.query(Url).filter(Url.url_id == url_id).first()

        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"URL with ID '{url_id}' not found"
            )

        all_urls = session.query(Url).all()

        # Calculate Levenshtein distance for each URL
        similarity_scores = [(other_url, distance(
            str(url.final_url), str(other_url.final_url))) for other_url in all_urls]

        # Sort by similarity scores
        sorted_similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1])

        # Filter out URLs that are below the threshold
        similar_urls_list = [other_url for other_url,
                             score in sorted_similarity_scores if score <= threshold and other_url.url_id is not url_id]

        # Limit the number of similar URLs to 5
        similar_urls_list = similar_urls_list[:5]

        if not latest:
            results = session.query(Result).filter(Result.url_id == url_id).order_by(
                desc(Result.datetime_created)).all()

            return {
                **url.__dict__,
                "results": [result.__dict__ for result in results],
                "similar_urls": [url.__dict__ for url in similar_urls_list]
            }
        else:
            result = session.query(Result).filter(Result.url_id == url_id).order_by(
                desc(Result.datetime_created)).first()

            return {
                **url.__dict__,
                "result": result.__dict__ if result else None,
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve URL info")


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


def retrieve_results(
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

        return {"total_count": total_count, "results": formatted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_result_with_features(result_id: int, session: Session):
    try:
        result_data = session.query(Result).\
            filter(Result.result_id == result_id).\
            first()

        if not result_data:
            raise HTTPException(
                status_code=404, detail="Result with 'result_id: {result_id}' not found")

        feature_data = session.query(Feature).\
            filter(Feature.feature_id == result_data.feature_id).\
            first()

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
        result_data = session.query(Result).filter(
            Result.submission_id == submission_id).all()

        if not result_data:
            raise HTTPException(
                status_code=404, detail="Result associated with 'submission_id: {submission_id}' not found")

        results = []

        for result in result_data:
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
        query_result = session.query(Submission,).\
            filter(Submission.submission_id == submission_id).\
            first()

        if not query_result:
            raise HTTPException(
                status_code=404, detail="Submission with 'submission_id: {submission_id}' not found")

        return query_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
