import asyncio

from asgi_lifespan import LifespanManager
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from app.core.config import settings
from app.database.db import get_async_session
from app.models.base import Base
from app.main import app

engine = create_async_engine(settings.postgres_db_url)
TestAsyncSession = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    """Returns a new event_loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport, base_url="http://localhost:8000"
    ) as client:
        async with LifespanManager(app):  # For pagination handling in tests
            yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db(get_test_data):
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSession() as session:
        session.add_all(get_test_data)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
async def override_get_db(init_test_db):
    async def _get_async_session():
        async with TestAsyncSession() as session:
            yield session

    app.dependency_overrides[get_async_session] = _get_async_session


pytest_plugins = [
    "tests.fixtures.instruments",
]
