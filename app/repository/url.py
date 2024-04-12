from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.urlresult import *


def create_ScanResult(url: str, result: URLresult, session: Session):
    try:
        scan_result = models.ScanResult(url,
                                        final_url=result.final_url,
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
        url_result = session.query(models.ScanResult).filter(
            models.ScanResult.scan_id == scan_id).first()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {scan_id}' in the database")
    return url_result

# CRUD for REPORT DB
def create_ReportResult(url: str, session: Session):
    try:
        report_result = models.ReportResult(url)                          
        session.add(report_result)
        session.commit()
        session.refresh(report_result)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new entry for '{url}' in the database")
    return report_result

def get_ReportResult(report_id: int, session: Session):
    try:
        report_result = session.query(models.ReportResult).filter(
        models.ReportResult.report_id == report_id).first()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {report_id}' in the database")
    return report_result

