from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.urlresult import *


def create_ScanResult(url: str, result: URLresult, session: Session):
    try:
        scan_result = models.ScanResult(url=url,
                                        final_url=result.get_final_url(),
                                        phish_prob=result.get_phish_prob(),
                                        is_phishing=result.get_isPhish())
        session.add(scan_result)
        session.commit()
        session.refresh(scan_result)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new entry for '{url}' in the database")
    return scan_result


def get_ScanResult(scan_id: int, session: Session):
    try:
        scan_result = session.query(models.ScanResult).filter(
            models.ScanResult.scan_id == scan_id).first()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {scan_id}' in the database")
    return scan_result


def search_url(final_url: str, session: Session):
    try:
        scan_result = session.query(models.ScanResult).filter(
            models.ScanResult.final_url == final_url).first()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to search for '{final_url}' in the database")
    return scan_result
