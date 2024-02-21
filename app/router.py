from fastapi import APIRouter
from app.models import ScanResult, ScanStatus

router = APIRouter()


@router.get("/scan/")
async def get_result(url: str):
    # This is where the processing logic should be...
    # Idea: return scan_id != 0 if the scan is successful.
    # Then, use that scan_id to fetch data w/ result/?scan_id=...
    # For now, let's scope the mechanism to work on only single URL per request first.
    scan_status = ScanStatus(url=url, scan_id=1)

    return scan_status


@router.get("/result/")
async def get_result(scan_id: int):
    # Result fetching logic with scan_id...
    result_data = {"url": "example.com"}
    scan_result = ScanResult(scan_id=scan_id, results=result_data)

    return scan_result
