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

    # ---------------------------------

    updated_date: datetime

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
    submission_id: int
    url_id: int
    feature_id: int
    submitted_url: str
    phish_prob: float
    phish_prob_mod: float
    has_soup: bool
    datetime_created: datetime

    # @validator('phish_prob', 'phish_prob_mod', pre=True)
    # @classmethod
    # def parse_extra_features(cls, value):
    #     if isinstance(value, float):
    #         return round(value*100, 2)
    #     return value

    @computed_field
    @property
    def trust_score(self) -> float:
        safe_prob = 1 - (self.phish_prob_mod/100)
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
    www: int | None   # 2
    subdomain: int | None #3
    https: int | None   #4
    short_url: int | None   #5
    at_count : int | None  #6
    dash_count: int | None   # 7
    equal_count: int | None   # 8
    dot_count: int | None   # 9
    underscore_count: int | None   #10
    slash_count: int | None   # 11
    digit_count: int | None #12  
    log_count: int | None  #13
    pay_count: int | None  #14
    web_count: int | None  #15
    account_count: int | None # 16
    pc_emptylink: float | None # 17
    pc_extlink: float | None  # 18
    pc_requrl: float | None   # 19
    zerolink: int | None   # 20
    ext_favicon: int | None   # 21
    submit2Email: int | None  # 22
    sfh: int | None   # 23
    redirection: int | None   #24
    domainage: int | None   # 25
    domainend: int | None   # 26


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

    # @validator('www', 'subdomain','https', 'short_url', 'zerolink', 'ext_favicon',
    #            'sfh','submit2Email', 'redirection','domainage', 'domainend', pre=True)
    # @classmethod
    # def cast_to_bool(cls, value: bool):
    #     if value == False:
    #         return False
    #     elif value == True:
    #         return True
    #     else:
    #         return None

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

class UrlSimilarUrlRequest(BaseModel):
    threshold: int
    amount: int
    
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
    

class UrlResultPaginatedRequest(BaseModel):
    page: int = 1
    page_size: int = 10
    sort_by: str | None
    sort_direction: str | None
    
class UrlResultPaginatedResponse(BaseModel):
    total_count: int
    results: list[ResultBase] = []
