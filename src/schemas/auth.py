from pydantic import BaseModel, ConfigDict, EmailStr


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
    sub: str
    iss: str
    iat: int
    exp: int
    nbf: int

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
