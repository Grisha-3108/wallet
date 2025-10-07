import uuid

import pytest_asyncio
from httpx import (AsyncClient,
                   ASGITransport)
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker)

from core.models import Base
from core.config import settings
from core.crud import create_wallet
from main import app


@pytest_asyncio.fixture(scope='session')
async def engine():
    # Запущен ли тестовый режим?
    assert settings.test_mode
    async_engine = create_async_engine(settings.test_db.postgre_connection_string,
                                       pool_size=settings.test_db.pool_size,
                                       max_overflow=settings.test_db.max_overflow,
                                       isolation_level=settings.db.isolation_level,
                                       connect_args = {'ssl': settings.db.ssl})
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return async_engine


@pytest_asyncio.fixture(scope='session')
async def db_sessionmaker(engine):
    return async_sessionmaker(bind=engine,
                              autoflush=False,
                              autocommit=False,
                              expire_on_commit=False)


@pytest_asyncio.fixture(scope='session')
async def single_wallet(db_sessionmaker):
    id = uuid.UUID('36440671-05ef-45e7-949d-ee0f534c5876')
    await create_wallet(id, session_factory=db_sessionmaker)


@pytest_asyncio.fixture(scope='session')
async def test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, 
                           base_url=str(settings.base_url)) as client:
        yield client