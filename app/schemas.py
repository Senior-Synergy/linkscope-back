# Pydantic model
from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import json
class Url_submission(BaseModel):
    submitted_url : str

class Url_submission_list(BaseModel):
    urls: List[str]

class Url(BaseModel):
    final_url: str
    hostname : str
    domain: str
    subdomains : Optional[str]
    scheme : Optional[str]
    # extra domain infomation
    creation_date : Optional[datetime]
    expiration_date : Optional[datetime]          
    domainage : int
    domainend : int
    city : Optional[str]
    state : Optional[str]
    country : Optional[str]
    google_safe_browsing : Optional[int]
 
    @field_validator('subdomains')
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)
   
   
class Feature(BaseModel): 
    domainlength : int #1
    www : bool  # 2    
    https : bool  # 3    
    short_url : bool  # 4
    ip : bool  # 5    
    dash_count : int  # 6
    equal_count : int  # 7
    dot_count : int # 8
    underscore_count: int  # 9
    slash_count : int  # 10
    digit_count : int  # 11   
    pc_emptylink : float  # 12
    pc_extlink : float # 13
    pc_requrl : float # 14
    zerolink : bool # 15
    ext_favicon : bool  # 16    
    sfh : bool  # 17
    redirection : bool  # 18   
    domainend : bool  # 19 

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
 
    @field_validator('www', 'https', 'short_url', 'ip', 
                     'zerolink', 'ext_favicon','sfh', 'redirection', 'domainend')
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
    #is_phishing: bool
    datetime_created: Optional[datetime]
    url: Url
    feature: Feature
    
    @field_validator('phish_prob')
    @classmethod
    def parse_extra_features(cls, value):
        if isinstance(value, float):
            return round(value*100, 2)
        return value

    class Config:
        from_attributes = True