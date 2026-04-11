from datetime import datetime
from sqlmodel import SQLModel, Field, func
from models.role import Role


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
