from __future__ import annotations

from functools import lru_cache
from typing import AsyncGenerator, Generator

from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.models.base import Base


class _DatabaseSettings:
    """Pulled from environment once at import-time."""

    SYNC_DATABASE_URL: str = settings.SYNC_DATABASE_URL
    ASYNC_DATABASE_URL: str = settings.ASYNC_DATABASE_URL
    DB_ECHO: bool = settings.DB_ECHO

    DB_CONNECT_ARGS = (
        {"check_same_thread": False} if SYNC_DATABASE_URL.startswith("sqlite") else {}
    )


db_settings = _DatabaseSettings()


def _configure_sqlite(engine: Engine) -> None:
    """
    For SQLite only:
    * Enable WAL mode (better concurrent writes).
    * Enforce foreign-key constraints.
    """
    if engine.dialect.name != "sqlite":
        return

    @event.listens_for(engine, "connect", once=True)
    def _set_sqlite_pragma(dbapi_conn, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


@lru_cache(maxsize=1)
def _make_sync_engine() -> Engine:
    engine = create_engine(
        db_settings.SYNC_DATABASE_URL,
        echo=db_settings.DB_ECHO,
        pool_pre_ping=True,
        connect_args=db_settings.DB_CONNECT_ARGS,
        future=True,
    )
    _configure_sqlite(engine)
    return engine


@lru_cache(maxsize=1)
def _make_async_engine() -> AsyncEngine:
    engine = create_async_engine(
        db_settings.ASYNC_DATABASE_URL,
        echo=db_settings.DB_ECHO,
        pool_pre_ping=True,
        connect_args=db_settings.DB_CONNECT_ARGS,
        future=True,
    )
    _configure_sqlite(engine.sync_engine)
    return engine


# ─── Global Engines and Session Factories ──────────────────────────────

sync_engine: Engine = _make_sync_engine()
async_engine: AsyncEngine = _make_async_engine()

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


# ─── Dependency for Sync Routes ────────────────────────────────────────

def get_sync_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ─── Dependency for Async Routes ───────────────────────────────────────

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ─── Run DB Migration / Init Tables ────────────────────────────────────

async def init_models(Base: Base) -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
