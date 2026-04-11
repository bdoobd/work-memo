from sqlmodel import SQLModel, Field


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str
