from fastapi import APIRouter

from .endpoints import scan

router = APIRouter()
router.include_router(scan.router, prefix="/scan", tags=["Scan"])
