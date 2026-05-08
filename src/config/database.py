from typing import AsyncGenerator

from src.config.settings import get_settings

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

settings = get_settings()

async_engine = create_async_engine(
    url=settings.async_postgresql_url,
    echo=settings.DEBUG,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)

session_maker = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def dispose_session() -> None:
    await async_engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with session_maker() as session:
            yield session
    except Exception:
        await async_engine.dispose()
