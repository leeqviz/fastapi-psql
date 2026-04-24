from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import UsersRepository
from src.schemas.auth import LoginSchema


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UsersRepository(self.session)

    async def get_user_credentials(self, name: str, email: str):
        user = await self.repo.get_with_roles(name, email)

        if not user:
            return None

        return LoginSchema(
            id=str(user.id),
            name=user.name,
            email=user.email,
            password=user.password.encode(),
            is_active=user.is_active,
            roles=[role.name for role in user.roles],
        )
