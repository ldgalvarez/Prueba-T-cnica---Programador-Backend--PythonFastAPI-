import os
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.db.session import AsyncSessionLocal, engine as prod_engine

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture(scope="session", autouse=True)
def test_db():
    # Use the same DATABASE_URL, but create a fresh schema per test session
    url = settings.DATABASE_URL
    engine = create_async_engine(url, future=True)
    async def prepare():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.get_event_loop().run_until_complete(prepare())
    yield
    async def teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.get_event_loop().run_until_complete(teardown())

@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
