from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, func, Relationship

if TYPE_CHECKING:
    from .role import Role


class BaseUser(SQLModel):
    username: str = Field(index=True)
    role_id: int = Field(foreign_key="role.id")


class WriteUser(BaseUser):
    password_hash: str


class User(WriteUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()}
    )
    modified: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
    disabled: bool = Field(default=False)

    role: "Role" = Relationship(back_populates="users")


class CreateUser(BaseUser):
    password: str
    password_confirm: str


class UpdateUser(SQLModel):
    role_id: int | None = None
    disabled: bool | None = None
    password_hash: str | None = None


class ShowUser(BaseUser):
    id: int = Field(primary_key=True)
    created: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()}
    )
    modified: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
    disabled: bool = Field(default=False)


class FindUser(SQLModel):
    username: str | None = None
    role: int | None = None
