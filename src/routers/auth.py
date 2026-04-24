from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs import settings
from src.db import get_psql_session
from src.schemas.auth import LoginRequest, LoginSchema, MeSchema, TokenSchema
from src.services.auth import AuthService
from src.utils.auth import (
    decode_jwt,
    issue_access_token,
    issue_refresh_token,
    validate_password,
)

http_bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    scheme_name="JWTAuth",
    description="JWT access token in the Authorization header",
    auto_error=True,
)
auth_router = APIRouter()


def get_auth_service(
    session: AsyncSession = Depends(get_psql_session),
) -> AuthService:
    return AuthService(session)


async def validate_login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginSchema:
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username, email or password",
    )
    user = await auth_service.get_user_credentials(payload.name, payload.email)
    if not user:
        raise unauth_ex
    if not validate_password(payload.password, user.password):
        raise unauth_ex
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


@auth_router.post("/login")
async def login(user: Annotated[LoginSchema, Depends(validate_login)]) -> TokenSchema:
    claims = {
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        "roles": user.roles,
    }
    access_token = issue_access_token(user.id, claims)
    refresh_token = issue_refresh_token(user.id, claims)
    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def get_auth_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MeSchema:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid",
    )
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise unauth_ex from e
    if payload.get("type") != "access" or payload.get("iss") != settings.app.name:
        raise unauth_ex

    user = MeSchema.model_validate(payload)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    db_user = await auth_service.get_user_credentials(user.name, user.email)
    if not db_user:
        raise unauth_ex

    return user


@auth_router.get("/me")
async def me(user: Annotated[MeSchema, Depends(get_auth_user)]) -> MeSchema:
    return user


async def validate_refresh(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginSchema:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid",
    )
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise unauth_ex from e
    if payload.get("type") != "refresh" or payload.get("iss") != settings.app.name:
        raise unauth_ex

    user = MeSchema.model_validate(payload)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    db_user = await auth_service.get_user_credentials(user.name, user.email)
    if not db_user:
        raise unauth_ex

    return db_user


@auth_router.post("/refresh", response_model_exclude_none=True)
async def refresh(
    user: Annotated[LoginSchema, Depends(validate_refresh)],
) -> TokenSchema:
    claims = {
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        "roles": user.roles,
    }
    access_token = issue_access_token(user.id, claims)
    return TokenSchema(
        access_token=access_token,
    )
