from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

if TYPE_CHECKING:
    from .user import User


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str

    users: list["User"] = Relationship(back_populates="role")

class ShowRole(SQLModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    role: str

class UpdateRole(SQLModel):
    role: str | None = None