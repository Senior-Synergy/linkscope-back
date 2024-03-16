from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.urlresult import *
from app.constants import feature_names2
from typing import List
import random
#-----------------------------------------CREATE--------------------------------------------------
# insert to url_submission table
def create_url_submission(session: Session): 
    try:
        #scan_id = random.randint(100000,999999)
        report_result = models.URLSubmission()
        session.add(report_result)
        session.commit()
        session.refresh(report_result)
    except Exception as e:
        print(f'Error to create_url_submission is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new submission for in the database")
    return report_result

# insert to url_result table
def create_url_result(url: str, scan_id: int, result: URLresult, session: Session):
    try:
        scan_result = models.URLResult(scan_id=scan_id, 
                                        url=url,
                                        final_url=result.get_final_url(),
                                        phish_prob=result.get_phish_prob(),
                                        is_phishing=result.get_isPhish())
        session.add(scan_result)
        session.commit()
        session.refresh(scan_result)
    except Exception as e:
        print(f'Error to insert to url_result is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create a new entry for '{url}' in the database")
    return scan_result

# insert to url_features table
def create_url_features(url_id : int, final_url : str, result: URLresult, session: Session):
    try:
        features_arr = result.features_arr
        # I will find way to shorten this ....
        feature_result = models.URLFeatures(url_id = url_id,
                                                final_url = final_url,
                                                domainlength = features_arr[0][0], #1
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
        session.add(feature_result)
        session.commit()
        session.refresh(feature_result)          
         
    except Exception as e:
        print(f'Error to insert url_features is {str(e)}')
        session.rollback()

#-----------------------------------------READ--------------------------------------------------
def search_url(final_url: str, session: Session):
    try:
        scan_result = session.query(models.URLResult).filter(
            models.URLResult.final_url == final_url).first()
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to search for '{final_url}' in the database")
        
    return scan_result

def get_url_result_by_url_id(url_id: int, session: Session):
    try:
        scan_result = session.query(models.URLResult).filter(
            models.URLResult.url_id == url_id).first()
    except Exception as e:
        print(f'Error to get url result by url_id is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {url_id}' in the database")
    return scan_result

# Error : get all url result by scan_id(PK of url_submission) 
def get_url_result_by_scan_id(scan_id: int, session: Session):
    try:
        report_result = session.query(models.URLResult).filter(
        models.URLResult.scan_id == scan_id).all()
        print(f'report_result is {report_result}')
    except Exception as e:
        print(f'error is {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to access 'scan_id: {scan_id}' in the database")
    #print(report_result)
    return report_result
