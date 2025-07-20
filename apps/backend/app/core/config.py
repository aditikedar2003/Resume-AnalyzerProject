from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    DB_ECHO: bool = False

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
