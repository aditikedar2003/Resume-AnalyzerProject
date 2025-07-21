from fastapi import FastAPI

from app.core.logging import setup_logging
from app.core.database import init_models, async_engine
from app.models.base import Base
from app.api import router as api_router  # Your API routes

# Set up logging once
setup_logging()

# Create FastAPI app instance
app = FastAPI(title="Resume Analyzer API")

# Run model creation on startup (Render PostgreSQL or local DB)
@app.on_event("startup")
async def on_startup():
    await init_models(Base)

# Include all API routes
app.include_router(api_router)
