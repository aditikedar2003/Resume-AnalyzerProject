from fastapi import APIRouter
from app.api.resume import resume_router
from app.api.user import user_router
from app.api.job import job_router

v1_router = APIRouter()

# Prefix v1 to all routes
v1_router.include_router(resume_router, prefix="/resume", tags=["Resume"])
v1_router.include_router(user_router, prefix="/user", tags=["User"])
v1_router.include_router(job_router, prefix="/job", tags=["Job"])
