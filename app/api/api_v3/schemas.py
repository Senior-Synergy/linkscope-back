from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import json


class SubmissionBase(BaseModel):
    submission_id: int
    datetime_submitted: datetime


class UrlBase(BaseModel):
    url_id: int
    final_url: str
    hostname: str
    domain: str
    subdomains: Optional[str]
    scheme: Optional[str]

    # ---------------------------------
    creation_date: Optional[datetime]
    expiration_date: Optional[datetime]
    domainage: Optional[int]
    domainend: Optional[int]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]

    @field_validator('subdomains')
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)


class ResultBase(BaseModel):
    result_id: int
    submission_id: Optional[int]
    url_id: Optional[int]
    feature_id: Optional[int]
    submitted_url: str
    phish_prob: float
    datetime_created: datetime

    @field_validator('phish_prob')
    @classmethod
    def parse_extra_features(cls, value):
        if isinstance(value, float):
            return round(value*100, 2)
        return value


class FeatureBase(BaseModel):
    feature_id: int
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

    # ---------------------------------
    shortten_url: Optional[str]
    ip_in_url: Optional[str]
    len_empty_links: int
    len_external_links: int
    external_links: Optional[str] = []
    external_img_requrl: Optional[str] = []
    external_audio_requrl: Optional[str] = []
    external_embed_requrl: Optional[str] = []
    external_iframe_requrl: Optional[str] = []
    len_external_img_requrl: int
    len_external_audio_requrl: int
    len_external_embed_requrl: int
    len_external_iframe_requrl: int

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

    @field_validator('pc_emptylink', 'pc_extlink', 'pc_requrl')
    @classmethod
    def round_float(cls, value: float):
        if value == -1:
            return None
        return round(value, 2)

    @field_validator('external_links', 'external_img_requrl', 'external_audio_requrl', 'external_embed_requrl', 'external_iframe_requrl')
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)


# --------------- API Response Models ---------------


class UrlExtended(UrlBase):
    results: Optional[ResultBase | list[ResultBase]] = []

    class Config:
        from_attributes = True


class ResultExtended(ResultBase):
    url: Optional[UrlBase]
    feature: Optional[FeatureBase]

    class Config:
        from_attributes = True


class SubmissionExtended(SubmissionBase):
    results: Optional[list[ResultExtended]] = []

    class Config:
        from_attributes = True


class SubmissionResult(BaseModel):
    submission_id: int


class SubmissionUrls(BaseModel):
    urls: list[str]


class UrlSearch(BaseModel):
    keyword: list[str]
