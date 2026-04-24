from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        return (await self.session.scalars(select(User))).all()

    async def get_by_id(self, user_id: UUID):
        return await self.session.get(User, user_id)

    async def get_with_roles(self, name: str, email: str):
        return (
            await self.session.scalars(
                select(User)
                .options(selectinload(User.roles))
                .where(User.name == name and User.email == email)
            )
        ).first()

    async def create(self, user: User):
        self.session.add(user)

    async def delete(self, user: User):
        await self.session.delete(user)
