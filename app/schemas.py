# Pydantic model
from typing import Union, List, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import json
class Url_submission(BaseModel):
    submitted_url : str

class Url_submission_list(BaseModel):
    urls: List[str]

class Url(BaseModel):
    final_url: str
    extra_features : dict
    whois_features : str
    
    # Convert json-formattes string to dict
    @field_validator('whois_features')
    def parse_extra_features(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value
class Feature(BaseModel):
    domainlength : int #1
    www : int  # 2
    subdomain : int  # 3
    https : int  # 4
    http : int  # 5
    short_url : int  # 6
    ip : int  # 7
    at_count : int  # 8
    dash_count : int  # 9
    equal_count : int  # 10
    dot_count : int # 11
    underscore_count: int  # 12
    slash_count : int  # 13
    digit_count : int  # 14
    log_contain : int  # 15
    pay_contain: int  # 16
    web_contain : int  #17
    cmd_contain : int  # 18
    account_contain : int  # 19
    pc_emptylink : float  # 20
    pc_extlink : float # 21
    pc_requrl : float # 22
    zerolink : int # 23
    ext_favicon : int  # 24
    submit_to_email : int  # 25
    sfh : int  # 26
    redirection : int  # 27
    domainage : int  # 28
    domainend : int  # 29 
    
    # Convert json-formattes string to dict
    @field_validator('pc_emptylink', 'pc_extlink', 'pc_requrl')
    def parse_extra_features(cls, value):
        if isinstance(value, float):
            return round(value, 2)
        return value 
class Result(BaseModel):
    url_id: int
    submitted_url: str
    phish_prob: float
    is_phishing: bool
    datetime_created: datetime
    url : Url
    feature : Feature
    
    @field_validator('phish_prob')
    def parse_extra_features(cls, value):
        if isinstance(value, float):
            return round(value*100, 2)
        return value
    class Config():
        from_attributes = True
