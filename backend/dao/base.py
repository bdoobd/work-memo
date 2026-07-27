from typing import TypeVar, Generic, Type, Annotated

from fastapi import Depends
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from .filter import Filter
from .expression_builder import builder

# from dao.session_builder import connection
# from session import AsyncSessionLocal

T = TypeVar("T")


class BaseDAO(Generic[T]):

    model: Type[T]

    @classmethod
    async def find_one(cls, session: AsyncSession, id: int):
        return await session.get(cls.model, id)

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filter: Filter):
        expr = builder(cls.model, filter)

        stmt = select(cls.model).where(expr)
        result = await session.exec(stmt)

        return result.one_or_none()

    @classmethod
    async def find(
        cls,
        session: AsyncSession,
        offset: int,
        limit: int,
        filters: list[Filter] | None = None,
    ):

        stmt = select(cls.model)

        if filters:
            expressions = [builder(cls.model, filter_) for filter_ in filters]

            stmt = stmt.where(*expressions)

        result = await session.exec(stmt.offset(offset=offset).limit(limit=limit))

        return result.all()

    @classmethod
    async def create(cls, data: BaseModel, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        instance = cls.model(**values)

        session.add(instance=instance)
        await session.flush()
        await session.refresh(instance=instance)

        return instance

    @classmethod
    async def update(cls, id: int, data: BaseModel, session: AsyncSession):

        found = await session.get(cls.model, id)

        if found is None:
            return None

        updates = data.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(found, key, value)

            session.add(found)
            await session.commit()
            await session.refresh(found)

        return found

    @classmethod
    async def delete(cls, id: int, session: AsyncSession):
        found = await session.get(cls.model, id)

        if found is None:
            return None

        await session.delete(found)
        await session.commit()

        return found
