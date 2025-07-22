# app/main.py
from fastapi import FastAPI
from app.core import setup_logging, init_models
from app.models.base import Base
from app.api.router import router as api_router


# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(title="Resume Analyzer API")

# On startup, initialize DB models
@app.on_event("startup")
async def on_startup():
    await init_models(Base)

# Include API routes
app.include_router(api_router)
