from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import AppException
from src.db import get_psql_session
from src.schemas.user import UserIn, UserOut
from src.services.users import UsersService

users_router = APIRouter()


def get_users_service(
    session: AsyncSession = Depends(get_psql_session),
) -> UsersService:
    return UsersService(session)


@users_router.get("/")
async def get_users(
    users_service: Annotated[UsersService, Depends(get_users_service)],
) -> list[UserOut]:
    return await users_service.get_all()


@users_router.get("/{user_id}")
async def get_user(
    user_id: UUID, users_service: Annotated[UsersService, Depends(get_users_service)]
) -> UserOut:
    return await users_service.get_by_id(user_id)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserIn, users_service: Annotated[UsersService, Depends(get_users_service)]
) -> UserOut:
    return await users_service.create(user)


@users_router.patch("/{user_id}")
async def update_user(
    user_id: UUID,
    user: UserIn,
    users_service: Annotated[UsersService, Depends(get_users_service)],
) -> UserOut:
    try:
        return await users_service.update(user_id, user)
    except AppException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from exc


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID, users_service: Annotated[UsersService, Depends(get_users_service)]
):
    try:
        await users_service.delete(user_id)
    except AppException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from exc
