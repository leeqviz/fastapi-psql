from pydantic import BaseModel, ConfigDict, EmailStr


class LoginSchema(BaseModel):
    name: str
    email: EmailStr
    password: bytes
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class MeSchema(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    iat: int
    exp: int

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
