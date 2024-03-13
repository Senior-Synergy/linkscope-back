from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.urlresult import *

'''
def get_all(db: Session):
    urls = db.query(models.ScanResult).all()
    return urls
'''

def create_ScanResult(request: schemas.ScanResultCreate, db: Session):
    # create model
    model = load_model("data/model_new.gzip")
    obj = URLresult(request.url, model)
    final_url = obj.get_final_url()
    url_result = db.query(models.ScanResult).filter(models.ScanResult.final_url == final_url)
    if url_result:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"URL with the url {request.url} is already created")
    new_url = models.ScanResult(url = request.url,
                            final_url = final_url, 
                            phish_prob = obj.get_phish_prob(),
                            is_phishing = obj.get_isPhish(),
                            is_active = 1)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url
   
def get_ScanResult(scan_id : int, db: Session):
    url_result = db.query(models.ScanResult).filter(models.ScanResult.scan_id == scan_id ).first()
    if not url_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"URL with the id {scan_id} is not found")
    return url_result
