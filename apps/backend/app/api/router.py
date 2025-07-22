from fastapi import APIRouter

router = APIRouter()

# ⬇️ Import *after* defining `router` to avoid circular import
from app.api import resume, user, job

router.include_router(resume.router, prefix="/resume", tags=["Resume"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(job.router, prefix="/job", tags=["Job"])
