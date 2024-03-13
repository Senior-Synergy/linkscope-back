#Pydantic model
from typing import Union, List, Optional
from pydantic import BaseModel

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
    time_created : str

    class Config():
        orm_mode = True

