# Pydantic model
from typing import Union, List, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, field_validator
from datetime import datetime
import json
class Url_submission(BaseModel):
    submitted_url : str

class Url_submission_list(BaseModel):
    urls: List[str]

class Url(BaseModel):
    final_url: str
    hostname : dict
    hostname : str
    domain: str
    subdomains : Optional[str]
    scheme : Optional[str]
    # extra domain infomation
    creation_date : datetime
    expiration_date : datetime          
    domainage : int
    domainend : int
    city : Optional[str]
    state : Optional[str]
    country : Optional[str]
 
    @field_validator('subdomains')
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)
   
   
  
class Feature(BaseModel):
    domainlength : int #1
    www : bool  # 2
    subdomain : bool  # 3
    https : bool  # 4
    http : bool  # 5
    short_url : bool  # 6
    ip : bool  # 7
    at_count : int  # 8
    dash_count : int  # 9
    equal_count : int  # 10
    dot_count : int # 11
    underscore_count: int  # 12
    slash_count : int  # 13
    digit_count : int  # 14
    log_contain : bool  # 15
    pay_contain: bool  # 16
    web_contain : bool  #17
    cmd_contain : bool  # 18
    account_contain : bool  # 19
    pc_emptylink : float  # 20
    pc_extlink : float # 21
    pc_requrl : float # 22
    zerolink : bool #23
    ext_favicon : bool  # 24
    submit_to_email : bool  # 25
    sfh : bool  # 26
    redirection : bool  # 27
    domainage : bool  # 28
    domainend : bool  # 29 

    shortten_url : Optional[str]
    ip_in_url : Optional[str]                       
    len_empty_links : int
    external_links  : Optional[str] 
    len_external_links  : int
    external_img_requrl : Optional[str]   
    external_audio_requrl: Optional[str] 
    external_embed_requrl: Optional[str] 
    external_iframe_requrl : Optional[str] 
    len_external_img_requrl : int
    len_external_audio_requrl: int
    len_external_embed_requrl : int
    len_external_iframe_requrl : int 
 
    @field_validator('www', 'subdomain', 'https', 'http', 'short_url', 'ip', 'log_contain', 
                     'pay_contain', 'web_contain', 'cmd_contain', 'account_contain', 'zerolink', 'ext_favicon', 
                     'submit_to_email', 'sfh', 'redirection', 'domainage', 'domainend')
    @classmethod
    def cast_to_bool(cls, value :bool):
        if value == False:
            return False
        elif value == True:
            return True
        else:
            return None   
          
    # Convert json-formattes string to dict
    @field_validator('pc_emptylink', 'pc_extlink', 'pc_requrl')
    @classmethod
    def round_float(cls, value: float):
        if value == -1:
            return None
        return round(value, 2)
        
    # Convert json-formattes string to dict
    @field_validator('external_links', 'external_img_requrl','external_audio_requrl','external_embed_requrl','external_iframe_requrl')
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)
    
  
class Result(BaseModel):
    url_id: int
    submitted_url: str
    phish_prob: float
    is_phishing: bool
    datetime_created: datetime
    url : Url
    feature : Feature
    
    @field_validator('phish_prob')
    @classmethod
    def parse_extra_features(cls, value):
        if isinstance(value, float):
            return round(value*100, 2)
        return value
    class Config():
        from_attributes = True
