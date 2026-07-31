from datetime import datetime
from pydantic import BaseModel, ConfigDict

from models.role import ShowRole


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    role_id: int


class User(BaseUser):

    id: int
    created: datetime
    modified: datetime
    disabled: bool


class ShowUser(User):
    role: ShowRole


class AddUser(BaseUser):
    password_hash: str


class CreateUser(BaseUser):
    password: str
    password_confirm: str


class UpdateUser(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    role_id: int | None = None
    disabled: bool | None = None


class UpdateUserPassowrds(UpdateUser):
    password: str | None = None
    password_confirm: str | None = None


class UpdateUserHash(UpdateUser):
    password_hash: str | None = None


class TokenUser(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
