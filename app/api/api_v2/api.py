from fastapi import APIRouter
from .endpoints import url

router = APIRouter()

router.include_router(url.router, prefix="/url", tags=["URL"])
