from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import psql_conn
from src.schemas.user import UserIn, UserOut
from src.services.users import UsersService

users_router = APIRouter()

def get_users_service(session: AsyncSession = Depends(psql_conn.get_session)) -> UsersService:
    return UsersService(session)

@users_router.get("/", response_model=list[UserOut])
async def get_users(users_service: UsersService = Depends(get_users_service)):
    return await users_service.get_all()

@users_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, users_service: UsersService = Depends(get_users_service)):
    return await users_service.get_by_id(user_id)

@users_router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, users_service: UsersService = Depends(get_users_service)):
    return await users_service.create(user)

@users_router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, user: UserIn, users_service: UsersService = Depends(get_users_service)):
    try:
        return await users_service.update(user_id, user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, users_service: UsersService = Depends(get_users_service)):
    try:
        await users_service.delete(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")