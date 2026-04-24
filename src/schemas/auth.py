from pydantic import BaseModel, ConfigDict, EmailStr

from src.configs import settings


class LoginRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    password: bytes
    is_active: bool = True
    roles: list[str]

    model_config = ConfigDict(from_attributes=True)


class MeSchema(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    roles: list[str]
    type: str
    sub: str
    iss: str
    jti: str
    iat: int
    exp: int
    nbf: int

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    token_type: str = settings.jwt.token_type
    access_token: str
    refresh_token: str | None = None
