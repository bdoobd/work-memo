from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str

    users: list["User"] = Relationship(back_populates="role")
