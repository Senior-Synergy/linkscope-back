from fastapi import APIRouter
from .endpoints import submission, url, result

router = APIRouter()

router.include_router(url.router, prefix="/url", tags=["URL V3"])
router.include_router(submission.router, prefix="/submission", tags=["SUBMISSION (scan) V3"])
router.include_router(result.router, prefix="/result", tags=["RESULT V3"])
