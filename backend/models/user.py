from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, func, Relationship

# from pydantic import ConfigDict

# from models.role import ShowRole

if TYPE_CHECKING:
    from .role import Role


# class BaseUser(SQLModel):
#     username: str = Field(index=True)
#     role_id: int = Field(foreign_key="role.id")


# class WriteUser(BaseUser):
#     password_hash: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    role_id: int = Field(foreign_key="role.id")
    password_hash: str
    created: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()}
    )
    modified: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
    disabled: bool = Field(default=False)

    role: "Role" = Relationship(back_populates="users")


# class CreateUser(BaseUser):
#     password: str
#     password_confirm: str


# class UpdateUser(SQLModel):
#     role_id: int | None = None
#     disabled: bool | None = None
#     password: str | None = None
#     password_confirm: str | None = None


# class ShowUser(BaseUser):
#     model_config: ConfigDict = ConfigDict(from_attributes=True)

#     id: int
#     created: datetime
#     modified: datetime
#     disabled: bool


# class ShowUserWithRole(ShowUser):
#     role: ShowRole | None = None


# class FindUser(SQLModel):
# username: str | None = None
# role: int | None = None
