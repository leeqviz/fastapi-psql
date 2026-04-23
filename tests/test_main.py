import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.models import User


@pytest.mark.asyncio(loop_scope="session")
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_users(client: AsyncClient):
    response = await client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_list(db_session: AsyncSession):
    users = await db_session.scalars(select(User))
    assert users.all() == []
