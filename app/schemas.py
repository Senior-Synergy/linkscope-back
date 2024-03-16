# Pydantic model
from typing import Union, List, Optional
from pydantic import BaseModel
from datetime import datetime

class Url(BaseModel):
    url : str

class Url_List(BaseModel):
    urls: List[str]

class Url_Result(Url):
    url_id: int
    final_url: str
    phish_prob: float
    is_phishing: bool
    is_active: bool
    time_submitted: datetime

    class Config():
        from_attributes = True

