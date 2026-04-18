import asyncio
import sys
from uuid import uuid4

from sqlalchemy import select

from src.db import psql_conn
from src.models import User
from src.models.role import Role
from src.models.user_role import UserRole

USERS_TO_SEED = [
    User(
        id=uuid4(),
        email="admin@example.com",
        name="admin",
        password="admin_password",  # noqa: S106
    ),
    User(
        id=uuid4(),
        email="master@example.com",
        name="master",
        password="master_password",  # noqa: S106
    ),
    User(
        id=uuid4(),
        email="user@example.com",
        name="user",
        password="user_password",  # noqa: S106
    ),
    User(
        id=uuid4(),
        email="guest@example.com",
        name="guest",
        password="guest_password",  # noqa: S106
    ),
]

ROLES_TO_SEED = [
    Role(
        id=uuid4(),
        name="admin",
    ),
    Role(
        id=uuid4(),
        name="master",
    ),
    Role(
        id=uuid4(),
        name="user",
    ),
    Role(
        id=uuid4(),
        name="guest",
    ),
]

USER_ROLES_TO_SEED = [
    UserRole(
        user_id=USERS_TO_SEED[0].id,
        role_id=ROLES_TO_SEED[0].id,
        granted_by="system",
    ),
    UserRole(
        user_id=USERS_TO_SEED[1].id,
        role_id=ROLES_TO_SEED[1].id,
        granted_by="system",
    ),
    UserRole(
        user_id=USERS_TO_SEED[2].id,
        role_id=ROLES_TO_SEED[2].id,
        granted_by="system",
    ),
    UserRole(
        user_id=USERS_TO_SEED[3].id,
        role_id=ROLES_TO_SEED[3].id,
        granted_by="system",
    ),
]


async def seed(flag: bool):
    async with psql_conn.session_maker() as session:
        user_roles_result = await session.scalars(select(UserRole))
        user_roles = user_roles_result.all()

        if len(user_roles) > 0:
            if not flag:
                print("Seeding skipped: user_roles table is not empty")
                return
            else:
                print("Seeding forced: user_roles table will be cleared")
                for user_role in user_roles:
                    await session.delete(user_role)
                await session.commit()

        users_result = await session.scalars(select(User))
        users = users_result.all()

        if len(users) > 0:
            if not flag:
                print("Seeding skipped: users table is not empty")
                return
            else:
                print("Seeding forced: users table will be cleared")
                for user in users:
                    await session.delete(user)
                await session.commit()

        roles_result = await session.scalars(select(Role))
        roles = roles_result.all()

        if len(roles) > 0:
            if not flag:
                print("Seeding skipped: roles table is not empty")
                return
            else:
                print("Seeding forced: roles table will be cleared")
                for role in roles:
                    await session.delete(role)
                await session.commit()

        session.add_all(ROLES_TO_SEED)
        session.add_all(USERS_TO_SEED)
        session.add_all(USER_ROLES_TO_SEED)
        await session.commit()
        print(
            f"Seeding completed: inserted {len(ROLES_TO_SEED)} roles, {len(USERS_TO_SEED)} users and {len(USER_ROLES_TO_SEED)} user_roles"
        )


# python -m scripts.seed
if __name__ == "__main__":
    flag = len(sys.argv) > 1 and sys.argv[1] == "--force"
    asyncio.run(seed(flag))
