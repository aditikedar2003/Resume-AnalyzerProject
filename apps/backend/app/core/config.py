import os
import logging
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume Matcher"

    # Absolute path to your frontend static files
    FRONTEND_PATH: str = os.path.join(os.path.dirname(__file__), "frontend", "assets")

    # For local frontend (React or Streamlit)
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # DATABASE URLs (both async and sync)
    SYNC_DATABASE_URL: Optional[str]
    ASYNC_DATABASE_URL: Optional[str]

    # Optional session encryption key (can be used with auth/session)
    SESSION_SECRET_KEY: Optional[str]

    # Show DB logs or not
    DB_ECHO: bool = False

    # Prevent pyc file generation
    PYTHONDONTWRITEBYTECODE: int = 1

    # Optional: ENV name for logging (local / staging / production)
    ENV: str = "local"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
