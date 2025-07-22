from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4

from app.api import v1_router
from app.core import (
    setup_logging,
    settings,
    custom_http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

# Set up logging and configuration
setup_logging()

app = FastAPI(
    title="Resume Analyzer API",
    description="API for uploading, analyzing, and improving resumes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware to add request ID to each request
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response

app.add_middleware(RequestIDMiddleware)

# Register API routers
app.include_router(v1_router, prefix="/api/v1")

# Exception handlers
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(ValueError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
