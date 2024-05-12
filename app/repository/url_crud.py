from typing import Optional
from sqlalchemy import and_, asc, desc, func, or_
from sqlalchemy.orm import Session
from Levenshtein import distance
from datetime import datetime

from app.models import Url, Result
from fastapi import HTTPException


def update_url_bulk(url_to_update: list[Url], session: Session):
    try:
        for url in url_to_update:
            session.merge(url)

        session.commit()
        return
    except Exception as e:
        session.rollback()


def update_url(url: Url, new_values: dict, session: Session):
    try:
        for key, value in new_values.items():
            setattr(url, key, value)

        return url
    except Exception as e:
        session.rollback()

# ---------------------------------------------------------------------------------------


def create_url(url: Url,  session: Session):
    try:
        url_data = url

        session.add(url_data)
        session.commit()

        return url_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_url_by_url_id(url_id, session: Session):
    try:
        url = session.query(Url).\
            filter(Url.url_id == url_id).\
            first()

        return url
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing URL data for ID '{url_id}': {str(e)}")


def retrieve_url_by_final_url(final_url: str, session: Session):
    try:
        url_result = session.query(Url).\
            filter(Url.final_url == final_url).\
            first()

        return url_result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing URL data for final URL '{final_url}': {str(e)}")


def retrieve_all_urls(session: Session):
    try:
        url_data = session.query(Url).all()
        return url_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving all URLs: {str(e)}")


def retrieve_similar_urls(db: Session, url_id, final_url, threshold: int = 5, amount: int = 5):
    try:
        all_urls = db.query(Url).all()

        # Calculate Levenshtein distance for each URL
        similarity_scores = [(other_url, distance(
            final_url, str(other_url.final_url))) for other_url in all_urls]

        # Sort by similarity scores
        sorted_similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1])

        # Filter out URLs that are below the threshold
        similar_urls_list = [other_url for other_url, score in sorted_similarity_scores if bool(
            score <= threshold) and bool(other_url.url_id != url_id)]

        # Limit the number of similar URLs to 5
        similar_urls_list = similar_urls_list[:amount]

        return similar_urls_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_filtered_paginated_urls(
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

        # Subquery to get the latest result for each URL
        latest_result_subq = session.query(
            Result.url_id,
            func.max(Result.datetime_created).label('max_datetime_created')
        ).group_by(Result.url_id).subquery()

        # Main query to join URL with the latest result
        query = session.query(Url, Result).join(
            Url, Url.url_id == Result.url_id
        ).join(
            latest_result_subq,
            and_(
                Result.url_id == latest_result_subq.c.url_id,
                Result.datetime_created == latest_result_subq.c.max_datetime_created
            )
        )

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

        for url, result in fetched_data:
            formatted_data.append({
                **url.__dict__,
                "result": {
                    **result.__dict__,
                }
            })

        return {"total_count": total_count, "urls": formatted_data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve results")
