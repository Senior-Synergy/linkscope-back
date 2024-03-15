from fastapi import APIRouter
from .endpoints import scan, result

router = APIRouter()

router.include_router(scan.router, prefix="/url/scan", tags=["Scan"])
router.include_router(result.router, prefix="/url/result", tags=["Result"])
