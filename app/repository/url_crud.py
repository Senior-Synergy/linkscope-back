from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.urlresult import *
from app.constants import feature_names2
from typing import List
import random
#-----------------------------------------CREATE--------------------------------------------------
# insert to submission table
def create_submission(session: Session): 
    try:
        #scan_id = random.randint(100000,999999)
        submission_data = models.Submission()
        session.add(submission_data)
        session.commit()
        session.refresh(submission_data)
    except Exception as e:
        print(f'Error to create_url_submission is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new submission_data")
    return submission_data


# insert to url table
def create_url(result: URLresult, session: Session):
    try:
        url_data = models.Url(final_url=result.get_final_url())
        session.add(url_data)
        session.commit()
        session.refresh(url_data)
    except Exception as e:
        print(f'Error to insert to url_result is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new url_data")
    return url_data

# insert to url_features table
def create_feature(result: URLresult, session: Session):
    try:
        features_arr = result.features_arr
        # I will find way to shorten this ....
        feature_data = models.Feature(domainlength = features_arr[0][0], #1
                                      www = features_arr[0][1], # 2
                                      subdomain = features_arr[0][2] , # 3
                                      https = features_arr[0][3] , # 4
                                      http = features_arr[0][4] , # 5
                                      short_url = features_arr[0][5] , # 6
                                      ip = features_arr[0][6] , # 7
                                      at_count = features_arr[0][7], # 8
                                      dash_count = features_arr[0][8] , # 9
                                      equal_count = features_arr[0][9] , # 10
                                      dot_count = features_arr[0][10] , # 11
                                      underscore_count = features_arr[0][11] , # 12
                                      slash_count = features_arr[0][12] , # 13
                                      digit_count= features_arr[0][13] , # 14
                                      log_contain = features_arr[0][14] , # 15
                                      pay_contain = features_arr[0][15], # 16
                                      web_contain = features_arr[0][16], #17
                                      cmd_contain = features_arr[0][17], # 18
                                      account_contain= features_arr[0][18], # 19
                                      pc_emptylink = features_arr[0][19] , # 20
                                      pc_extlink = features_arr[0][20], # 21
                                      pc_requrl= features_arr[0][21] , # 22
                                      zerolink = features_arr[0][22] , # 23
                                      ext_favicon = features_arr[0][23], # 24
                                      submit_to_email = features_arr[0][24] , # 25
                                      sfh = features_arr[0][25] , # 26
                                      redirection = features_arr[0][26], # 27
                                      domainage = features_arr[0][27] , # 28
                                      domainend = features_arr[0][28] ) # 29 
        session.add(feature_data)
        session.commit()
        session.refresh(feature_data)          
         
    except Exception as e:
        print(f'Error to insert to url_result is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new feature_data")
    return feature_data

# insert to result table
def create_result(submission_id :int, url_id : int, feature_id : int, submitted_url : str, result: URLresult, session: Session):
    try:
        result_data = models.Result(submission_id=submission_id,
                                     url_id = url_id,
                                     feature_id = feature_id,
                                     submitted_url = submitted_url,
                                     phish_prob=result.get_phish_prob(),
                                    is_phishing=result.get_isPhish())
        session.add(result_data)
        session.commit()
        session.refresh(result_data)
    except Exception as e:
        print(f'Error to insert to url_result is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new result_data")
    return result_data


#-------------------------------------Bulk Insert-----------------------------------------------
def create_all(submission_data : models.Submission, url_objects : List[models.Url], feature_objects : List[models.Feature], result_objects : List[models.Result], session: Session):
    try: 
        session.add(submission_data)
        session.add_all(url_objects)
        session.add_all(feature_objects)
        session.add_all(result_objects)
        session.commit()
        #session.refresh()
    except Exception as e:
        print(f'Error to insert to url_result is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create all")
    return submission_data.submission_id


#-----------------------------------------READ--------------------------------------------------

def search_url(final_url: str, session: Session):
    try:
        scan_result = session.query(models.Url).filter(
            models.Url.final_url == final_url).first()
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to search for '{final_url}' in the database")
        
    return scan_result
''' 
def get_url_data_by_url_id(url_id: int, session: Session):
    try:
        scan_result = session.query(models.URLResult).filter(
            models.URLResult.url_id == url_id).first()
    except Exception as e:
        print(f'Error to get url result by url_id is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {url_id}' in the database")
    return scan_result
'''
def get_url_data_by_submission_id(submission_id: int, session: Session):
    try:
        url_result = session.query(models.Result).join(
            models.Url, models.Url.url_id == models.Url.url_id).filter(
            models.Result.submission_id == submission_id)
        print(url_result)
    except Exception as e:
        print(f'error is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {submission_id}' in the database")
    return url_result

'''
# How to join Syntax
   url_result = session.query(models.Url).join(
            models.Result, models.Result.url_id == models.Url.url_id).filter(
            models.Result.submission_id == submission_id
            )
'''