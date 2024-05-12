from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from datetime import datetime
from typing import Optional

from app.models import Result, Url


def create_result(result: Result,  session: Session):
    try:
        session.add(result)
        session.commit()
        session.refresh(result)

        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_latest_result_by_url_id(url_id, session: Session):
    try:
        result_data = session.query(Result).\
            filter(Result.url_id == url_id).\
            first()
        return result_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve result by URL ID")


def retrieve_all_results_by_url_id(url_id, session: Session):
    try:
        result_data = session.query(Result).\
            filter(Result.url_id == url_id).\
            all()
        return result_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve result by URL ID")


def retrieve_paginated_results_by_url_id(
    session: Session,
    url_id,
    page,
    page_size,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = 'desc'
):
    try:
        offset = (page - 1) * page_size
        query = session.query(Result, Url).join(
            Url, Result.url_id == Url.url_id)

        query = query.filter(Url.url_id == url_id)

        # Sorting
        if sort_by:
            model_class = Url if sort_by in Url.__table__.columns.keys() else Result
            sort_column = getattr(model_class, sort_by, None)
            if sort_column:
                sort_method = asc if sort_direction == 'asc' else desc
                query = query.order_by(sort_method(sort_column))
            else:
                raise ValueError(f"Invalid sort column '{sort_by}'")

        total_count = query.count()
        fetched_data = query.offset(offset).limit(page_size).all()

        # Convert fetched data into a list of dictionaries
        formatted_data = []

        for result, _ in fetched_data:
            formatted_data.append({
                **result.__dict__,
            })

        return {"total_count": total_count, "results": formatted_data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve results")


def retrieve_results_by_submission_id(submission_id, session: Session):
    try:
        result_data = session.query(Result).\
            filter(Result.submission_id == submission_id).\
            all()
        return result_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve result by submission ID")


def retrieve_filtered_paginated_results(
    session: Session,
    keyword: str,
    page,
    page_size,
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
            model_class = Url if sort_by in Url.__table__.columns.keys() else Result
            sort_column = getattr(model_class, sort_by, None)
            if sort_column:
                sort_method = asc if sort_direction == 'asc' else desc
                query = query.order_by(sort_method(sort_column))
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
            })

        return {"total_count": total_count, "results": formatted_data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve results")


def retrieve_result(result_id, session: Session):
    try:
        result_data = session.query(Result).\
            filter(Result.result_id == result_id).\
            first()

        return result_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve result with features")
