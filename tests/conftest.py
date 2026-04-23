import os

# Set ENV_STATE to "test" to use test database with .env.test
os.environ["ENV_STATE"] = "test"

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient

from src.configs import settings
from src.db import DatabaseConnection, get_psql_session
from src.main import app

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

psql_test_conn = DatabaseConnection(
    url=settings.postgres.url,
    echo=settings.postgres.echo,
    echo_pool=settings.postgres.echo_pool,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.postgres.url)
    command.upgrade(config, "head")
    yield  # tests run
    command.downgrade(config, "base")


@pytest_asyncio.fixture(name="db_session")
async def get_psql_session_test():
    async with psql_test_conn.session_maker() as session:
        yield session
        await session.rollback()
        # await session.close()


@pytest_asyncio.fixture
async def client(db_session):
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_psql_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
