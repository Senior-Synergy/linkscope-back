from pydantic import BaseModel


class Url(BaseModel):
    url: str


class Result(Url):
    is_phishing: bool


class ScanStatus(Url):
    scan_id: int


class ScanResult(BaseModel):
    scan_id: int
    results: Result
