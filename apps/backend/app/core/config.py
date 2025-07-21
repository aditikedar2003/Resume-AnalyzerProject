# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str

    SESSION_SECRET_KEY: str
    DB_ECHO: bool = False  # 👈 this must be bool, not str

    class Config:
        env_file = ".env"

# 👇 THIS MUST BE AT THE VERY END
settings = Settings()
