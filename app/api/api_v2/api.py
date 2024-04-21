from fastapi import APIRouter
from .endpoints import scan, result

router = APIRouter()

router.include_router(scan.router, prefix="/url/scan", tags=["Scan V2"])
router.include_router(result.router, prefix="/url/result", tags=["Result V2"])
