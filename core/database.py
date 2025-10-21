from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    async_sessionmaker, 
                                    AsyncSession)


from core.config import settings


async_engine = create_async_engine(
    settings.test_db.postgre_connection_string
    if settings.test_mode
    else settings.db.postgre_connection_string,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    isolation_level=settings.test_db.isolation_level,
    connect_args={"ssl": settings.test_db.ssl},
)


async_session_factory: AsyncGenerator[AsyncSession] = async_sessionmaker(
    bind=async_engine, autoflush=False, autocommit=False, expire_on_commit=False
)
