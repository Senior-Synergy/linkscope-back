from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Url, Feature, Result, Submission


def create_submission_bulk(submission_data: Submission, url_objects: list[Url], feature_objects: list[Feature], result_objects: list[Result], session: Session):
    try:
        session.add(submission_data)
        session.add_all(url_objects)
        session.add_all(feature_objects)
        session.add_all(result_objects)
        session.commit()

        return submission_data.submission_id
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_submission(submission_id, session: Session):
    try:
        submission_data = session.query(Submission).\
            filter(Submission.submission_id == submission_id).\
            first()

        return submission_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def create_submission(session: Session):
    try:
        submission_data = Submission()

        session.add(submission_data)
        session.commit()

        return submission_data.submission_id
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_submission_info(submission_id, session: Session):
    try:
        submission_data = session.query(Submission).filter(
            Submission.submission_id == submission_id).first()

        return submission_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
