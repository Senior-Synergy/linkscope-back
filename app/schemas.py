# Pydantic model
from typing import Union, List, Optional
from pydantic import BaseModel
from datetime import datetime


class UrlReport(BaseModel):
    urls: List[str]

class Url(BaseModel):
    url: str
    
class ScanResult(Url):
    url_id: int
    final_url: str
    phish_prob: float
    is_phishing: bool
    is_active: bool
    time_created: datetime

    class Config():
        from_attributes = True



