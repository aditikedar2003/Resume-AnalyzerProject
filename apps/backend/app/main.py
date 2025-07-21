from fastapi import FastAPI
from core import setup_logging, init_models, async_engine

from app.api import router as api_router  # Assuming you have routes inside /api

setup_logging()

app = FastAPI(title="Resume Analyzer API")

@app.on_event("startup")
async def on_startup():
    await init_models(Base)  # This creates tables if they don't exist

app.include_router(api_router)
