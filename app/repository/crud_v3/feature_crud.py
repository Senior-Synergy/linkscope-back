import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Feature


logger = logging.getLogger(__name__)


def retrieve_feature(feature_id: int, session: Session):
    try:
        feature_data = session.query(Feature).filter(
            Feature.feature_id == feature_id).first()

        if not feature_data:
            logger.error(f"Feature with ID {feature_id} not found")
            raise HTTPException(status_code=404, detail="Feature not found")

        return feature_data
    except Exception as e:
        logger.error(f"Failed to retrieve feature with ID {feature_id}: {e}")

        raise HTTPException(status_code=500, detail=str(e))
