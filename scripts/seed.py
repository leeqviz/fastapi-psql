import asyncio
from uuid import uuid4

from sqlalchemy import func, select

from src.db import psql_conn
from src.models import User

USERS_TO_SEED = [
    User(
        id=uuid4(),
        email="admin@example.com",
        name="admin",
        password="admin_password",  # noqa: S106
    ),
    User(
        id=uuid4(),
        email="user1@example.com",
        name="user1",
        password="user1_password",  # noqa: S106
    ),
    User(
        id=uuid4(),
        email="user2@example.com",
        name="user2",
        password="user2_password",  # noqa: S106
    ),
]


async def seed():
    async with psql_conn.session_maker() as session:
        result = await session.execute(select(func.count(User.id)))
        users_count = result.scalar_one()

        if users_count > 0:
            print("Seed skipped: users table is not empty")
            return

        session.add_all(USERS_TO_SEED)
        await session.commit()
        print(f"Seed completed: inserted {len(USERS_TO_SEED)} users")


# python -m src.scripts.seed
if __name__ == "__main__":
    asyncio.run(seed())
