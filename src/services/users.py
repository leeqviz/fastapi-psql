from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.users import UsersRepository
from src.schemas.user import UserIn, UserOut


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UsersRepository(self.session)
        
    async def get_all(self):
        users = await self.repo.get_all()
        return [UserOut.model_validate(user) for user in users]
    
    async def get_by_id(self, user_id: UUID):
        user = await self.repo.get_by_id(user_id)
        return UserOut.model_validate(user)
    
    async def create(self, user: UserIn):
        new_user = User(**user.model_dump(), id=uuid4())
        await self.repo.create(new_user)
        await self.session.commit()
        # await self.session.refresh(new_user)
        return new_user
    
    async def update(self, user_id: UUID, user: UserIn):
        
        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise Exception("User not found")
        
        db_user.name = user.name if user.name is not None else db_user.name
        db_user.email = user.email if user.email is not None else db_user.email
        db_user.password = user.password is not None if user.password else db_user.password
        await self.session.commit()
        return UserOut.model_validate(db_user)
    
    async def delete(self, user_id: UUID):
        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise Exception("User not found")
        
        await self.repo.delete(db_user)
        await self.session.commit()