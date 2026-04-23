from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class UserOut(UserSchema):
    id: UUID

    # optional
    model_config = ConfigDict(from_attributes=True)


class UserIn(UserSchema):
    pass


class UserAuth(UserSchema):
    is_active: bool = True
    model_config = ConfigDict(strict=True)
