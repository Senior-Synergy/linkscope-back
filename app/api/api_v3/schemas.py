from pydantic import BaseModel, validator, computed_field
from datetime import datetime
import json


class SubmissionBase(BaseModel):
    submission_id: int
    datetime_submitted: datetime


class UrlBase(BaseModel):
    url_id: int
    final_url: str
    hostname: str | None
    domain: str | None
    subdomains: list[str] | None
    scheme: str | None
    registrar: str | None
    ip_address: str | None

    # ---------------------------------

    creation_date: datetime | None
    expiration_date: datetime | None
    domainage: int | None
    domainend: int | None
    city: str | None
    state: str | None
    country: str | None
    google_is_malicious: bool | None

    @validator('subdomains', pre=True)
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)

    @validator('google_is_malicious', pre=True)
    @classmethod
    def cast_to_bool(cls, value: bool):
        if value == False:
            return False
        elif value == True:
            return True
        else:
            return None


class ResultBase(BaseModel):
    result_id: int
    submission_id: int | None
    url_id: int | None
    feature_id: int | None
    submitted_url: str
    phish_prob: float
    phish_prob_mod : float
    has_soup : bool | None
    #verdict: str | None
    datetime_created: datetime 

    @validator('phish_prob','phish_prob_mod', pre=True)
    @classmethod
    def parse_extra_features(cls, value):
        if isinstance(value, float):
            return round(value*100, 2)
        return value
    
    @computed_field
    @property
    def trust_score(self) -> float:
        safe_prob = 1 -(self.phish_prob_mod/100) 
        score = (safe_prob) * 5
        return round(score, 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.has_soup:
            if self.phish_prob_mod < 0.2:
                return "VERY_LOW"
            elif self.phish_prob_mod < 0.4:
                return "LOW"
            elif self.phish_prob_mod < 0.6:
                return "MEDIUM"
            elif self.phish_prob_mod < 0.8:
                return "HIGH"
            else:
                return "VERY_HIGH"
        else:
            return "UNKNOWN"  


class FeatureBase(BaseModel):
    feature_id: int
    domainlength: int | None   # 1
    www: bool | None   # 2
    https: bool | None   # 3
    short_url: bool | None   # 4
    ip: bool | None   # 5
    dash_count: int | None   # 6
    equal_count: int | None   # 7
    dot_count: int | None   # 8
    underscore_count: int | None   # 9
    slash_count: int | None   # 10
    digit_count: int | None   # 11
    pc_emptylink: float | None  # 12
    pc_extlink: float | None   # 13
    pc_requrl: float | None   # 14
    zerolink: bool | None   # 15
    ext_favicon: bool | None   # 16
    sfh: bool | None   # 17
    redirection: bool | None   # 18
    domainend: bool | None   # 19

    # ---------------------------------

    shortten_url: str | None
    ip_in_url: str | None
    empty_links_count: int | None
    external_links: list[str] | None
    external_img_requrl: list[str] | None
    external_audio_requrl: list[str] | None
    external_embed_requrl: list[str] | None
    external_iframe_requrl: list[str] | None
    len_external_links: int | None
    len_external_img_requrl: int | None
    len_external_audio_requrl: int | None
    len_external_embed_requrl: int | None
    len_external_iframe_requrl: int | None

    @validator('www', 'https', 'short_url', 'ip',
               'zerolink', 'ext_favicon',
               'sfh', 'redirection', 'domainend', pre=True)
    @classmethod
    def cast_to_bool(cls, value: bool):
        if value == False:
            return False
        elif value == True:
            return True
        else:
            return None

    @validator('pc_emptylink', 'pc_extlink', 'pc_requrl', pre=True)
    @classmethod
    def round_float(cls, value: float):
        if value == -1:
            return None
        return round(value, 2)

    @validator('external_links', 'external_img_requrl', 'external_audio_requrl', 'external_embed_requrl', 'external_iframe_requrl', pre=True)
    @classmethod
    def json_dumps(cls, value: str):
        if value is None:
            return None
        return json.loads(value)


# --------------- API Response Models ---------------


class Url(UrlBase):
    result: ResultBase | None = None

    class Config:
        from_attributes = True


class UrlExtended(UrlBase):
    results: ResultBase | list[ResultBase] | None = []
    similar_urls: list[UrlBase]

    class Config:
        from_attributes = True


class Result(ResultBase):
    url: UrlBase | None

    class Config:
        from_attributes = True


class ResultExtended(ResultBase):
    url: UrlBase | None
    feature: FeatureBase | None

    class Config:
        from_attributes = True


class ResultCreateRequest(BaseModel):
    submission_id: int
    url: str


class ResultCreateResponse(BaseModel):
    result_id: int


class Submission(SubmissionBase):
    results: list[Result] | None = []

    class Config:
        from_attributes = True


class SubmissionResponse(BaseModel):
    submission_id: int


class SubmissionCreateResponse(BaseModel):
    submission_id: int


class SubmissionRequest(BaseModel):
    urls: list[str]


class ResultSearchRequest(BaseModel):
    keyword: str
    page: int = 1
    page_size: int = 10
    creation_date_start: datetime | None
    creation_date_end: datetime | None
    phish_prob_min: float | None
    phish_prob_max: float | None
    country: str | None
    sort_by: str | None
    sort_direction: str | None


class ResultSearchResponse(BaseModel):
    total_count: int
    results: list[Result] = []


class UrlSearchRequest(BaseModel):
    keyword: str
    page: int = 1
    page_size: int = 10
    creation_date_start: datetime | None
    creation_date_end: datetime | None
    phish_prob_min: float | None
    phish_prob_max: float | None
    country: str | None
    sort_by: str | None
    sort_direction: str | None


class UrlSearchResponse(BaseModel):
    total_count: int
    urls: list[Url] = []
