import os
os.environ["APP_ENV"] = "test"

import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.main import app
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

from typing import AsyncGenerator

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
