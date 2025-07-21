# app/main.py

from fastapi import FastAPI
from app.core.logging import setup_logging   # ✅ Logging import
from app.core.database import init_models, async_engine
from app.models.base import Base
from app.api import router as api_router

# ✅ Call the logging setup once
setup_logging()

# FastAPI app
app = FastAPI(title="Resume Analyzer API")

# ✅ Run DB model creation on startup
@app.on_event("startup")
async def on_startup():
    await init_models(Base)

# ✅ Add all your API routes
app.include_router(api_router)
