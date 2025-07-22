from fastapi import APIRouter
from app.api import resume, user, job  # 👈 your route files

router = APIRouter()

router.include_router(resume.router, prefix="/resume", tags=["Resume"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(job.router, prefix="/job", tags=["Job"])
