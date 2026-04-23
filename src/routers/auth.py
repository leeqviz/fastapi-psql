from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs import settings
from src.db import get_psql_session
from src.schemas.auth import LoginSchema, MeSchema, TokenSchema
from src.services.auth import AuthService
from src.utils.auth import create_access_token, decode_jwt, validate_password

http_bearer = HTTPBearer()
auth_router = APIRouter()


def get_auth_service(
    session: AsyncSession = Depends(get_psql_session),
) -> AuthService:
    return AuthService(session)


async def validate_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username, email or password",
    )
    user = await auth_service.get_by_name_and_email(name, email)
    if not user:
        raise unauth_ex
    if not validate_password(password, user.password):
        raise unauth_ex
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return LoginSchema.model_validate(user)


@auth_router.post("/login")
async def login(user: Annotated[LoginSchema, Depends(validate_login)]) -> TokenSchema:
    payload = {
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
    }
    token = create_access_token(payload)
    return TokenSchema(access_token=token, token_type=settings.jwt.token_type)


async def get_auth_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MeSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        ) from e
    user = MeSchema.model_validate(payload)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    db_user = await auth_service.get_by_name_and_email(user.name, user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )

    return user


@auth_router.get("/me")
async def me(user: Annotated[MeSchema, Depends(get_auth_user)]) -> MeSchema:
    return user
