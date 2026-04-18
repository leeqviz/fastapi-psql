import os

# Set ENV_STATE to "test" to use test database with .env.test
os.environ["ENV_STATE"] = "test"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.configs import settings
from src.db import DatabaseConnection, get_psql_session
from src.main import app
from src.models import Base

psql_test_conn = DatabaseConnection(
    url=settings.postgres.url,
    echo=settings.postgres.echo,
    echo_pool=settings.postgres.echo_pool,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
)


@pytest_asyncio.fixture
async def get_psql_session_test():
    async with psql_test_conn.session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_db():
    async with psql_test_conn.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with psql_test_conn.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(get_psql_session_test):
    def override_get_session():
        yield get_psql_session_test

    app.dependency_overrides[get_psql_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
