from sqlalchemy.orm import Session
from sqlalchemy import update
from app.models import Url, Feature, Result, Submission
from fastapi import HTTPException, status
from app.urlresult import *


# -------------------------------------Create : Bulk Insert-----------------------------------------------


def create_all_result(submission_data: Submission, url_objects: list[Url], feature_objects: list[Feature], result_objects: list[Result], session: Session):
    try:
        session.add(submission_data)
        session.add_all(url_objects)
        session.add_all(feature_objects)
        session.add_all(result_objects)
        session.commit()

    except Exception as e:
        print(f'Error to insert to db is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create all")
    return submission_data.submission_id


# -----------------------------------------READ-----------------------------------------------------------


def search_url(final_url: str, session: Session):
    try:
        url_result = session.query(Url).filter(
            Url.final_url == final_url).first()

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to search for '{final_url}' in the database")

    return url_result


def get_all_result_by_submission_id(submission_id: int, session: Session):
    try:
        url_result = session.query(Result).join(
            Url, Url.url_id == Url.url_id).filter(
            Result.submission_id == submission_id).all()
    except Exception as e:
        print(f'error is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'submission_id: {submission_id}' in the database")
    return url_result


def get_url_data_by_url_id(url_id: int, session: Session):
    try:
        url = session.query(Url).filter(
            Url.url_id == url_id).first()
    except Exception as e:
        print(f'Error to get url result by url_id is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {url_id}' in the database")
    return url


# ----------------------------------------- Update : Bulk update -----------------------------------------------------------


def update_url_db(url_2update: list[Url], session: Session):
    try:

        session.execute(
            update(Url),
            url_2update
        )
        print('done update')
    except Exception as e:
        print(f'Error to update to db is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create all")
