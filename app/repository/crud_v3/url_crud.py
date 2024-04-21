from sqlalchemy.orm import Session
from Levenshtein import distance

from app.models import Url
from fastapi import HTTPException


def update_url_data(url_to_update: list[Url], session: Session):
    try:
        for url in url_to_update:
            session.merge(url)

        session.commit()
    except Exception as e:
        session.rollback()


# ---------------------------------------------------------------------------------------


def retrieve_url_by_url_id(url_id: int, session: Session):
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


def retrieve_similar_urls(db: Session, url_id: int, final_url: str, threshold: int = 5):
    try:
        all_urls = db.query(Url).all()

        # Calculate Levenshtein distance for each URL
        similarity_scores = [(other_url, distance(
            final_url, other_url.final_url)) for other_url in all_urls]

        # Sort by similarity scores
        sorted_similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1])

        # Filter out URLs that are below the threshold
        similar_urls_list = [other_url for other_url,
                             score in sorted_similarity_scores if score <= threshold and other_url.url_id != url_id]

        # Limit the number of similar URLs to 5
        similar_urls_list = similar_urls_list[:5]

        return similar_urls_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
