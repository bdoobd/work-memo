from typing import Any
from sqlmodel import SQLModel


class Filter(SQLModel):
    field: str
    operator: str
    value: str
