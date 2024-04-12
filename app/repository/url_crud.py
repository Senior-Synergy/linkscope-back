from sqlalchemy.orm import Session
from sqlalchemy import update
from app import models, schemas
from fastapi import HTTPException, status
from app.urlresult import *
from app.constants import feature_names_2
from typing import List
import random
#-------------------------------------Create : Bulk Insert-----------------------------------------------
def create_all_result(submission_data : models.Submission, url_objects : List[models.Url], feature_objects : List[models.Feature], result_objects : List[models.Result], session: Session):
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


#-----------------------------------------READ-----------------------------------------------------------

def search_url(final_url: str, session: Session):
    try:
        url_result = session.query(models.Url).filter(
            models.Url.final_url == final_url).first()
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to search for '{final_url}' in the database")
        
    return url_result

def get_all_result_by_submission_id(submission_id: int, session: Session):
    try:
        url_result = session.query(models.Result).join(
            models.Url, models.Url.url_id == models.Url.url_id).filter(
            models.Result.submission_id == submission_id).all()
    except Exception as e:
        print(f'error is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'submission_id: {submission_id}' in the database")
    return url_result



def get_url_data_by_url_id(url_id: int, session: Session):
    try:
        scan_result = session.query(models.Url).filter(
            models.Url.url_id == url_id).first()
        url_id = scan_result.url_id
    except Exception as e:
        print(f'Error to get url result by url_id is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {url_id}' in the database")
    return scan_result
#----------------------------------------- Update : Bulk update -----------------------------------------------------------
def update_url_db(url_2update: List[models.Url], session: Session):
    try:
        
        session.execute(
            update(models.Url),
            url_2update
        )
        print('done update')
    except Exception as e:
        print(f'Error to update to db is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create all")
   