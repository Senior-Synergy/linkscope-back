from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Feature


def create_feature(feature: Feature,  session: Session):
    try:
        feature_data = feature

        session.add(feature_data)
        session.commit()

        return feature_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_feature(feature_id, session: Session):
    try:
        feature_data = session.query(Feature).filter(
            Feature.feature_id == feature_id).first()

        if not feature_data:
            raise HTTPException(status_code=404, detail="Feature not found")

        return feature_data
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
