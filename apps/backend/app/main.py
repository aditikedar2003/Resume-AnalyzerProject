from fastapi import FastAPI
from app.core.logging import setup_logging         # ✅ correct now
from app.core.database import init_models, async_engine
from app.models.base import Base
from app.api import router as api_router

# Set up logging
setup_logging()

# FastAPI app
app = FastAPI(title="Resume Analyzer API")

# Run model creation on startup
@app.on_event("startup")
async def on_startup():
    await init_models(Base)

# Include all API routes
app.include_router(api_router)
