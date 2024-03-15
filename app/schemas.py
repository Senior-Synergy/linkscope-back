# Pydantic model
from typing import Union, List, Optional
#Afrom datetime import datetime
from pydantic import BaseModel, validator
from datetime import datetime

# model
class ScanResultBase(BaseModel):
    url: str
    

class ScanResultCreate(ScanResultBase):
    url : str


class  ScanResult(ScanResultBase):
    scan_id: int
    final_url : str
    phish_prob: float
    is_phishing: bool
    is_active : bool
    time_created : datetime

    class Config():
        from_attributes = True

