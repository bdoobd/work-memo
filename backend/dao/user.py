from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from fastapi import HTTPException

from .base import BaseDAO
from models.user import User

from dao.filter import Filter


class UserDAO(BaseDAO[User]):

    model = User

    @classmethod
    async def find(cls, session: AsyncSession, offset: int, limit: int):

        stmt = select(cls.model).options(selectinload(cls.model.role)).offset(offset=offset).limit(limit=limit)  # type: ignore[arg-type]

        result = await session.exec(stmt)
        users = result.all()

        if not users:
            raise HTTPException(status_code=404, detail="Users not found")

        return users

    @classmethod
    async def find_one(cls, session: AsyncSession, id: int):
        stmt = select(cls.model).options(selectinload(User.role)).where(cls.model.id == id)  # type: ignore[arg-type]

        result = await session.exec(stmt)

        user = result.first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    @classmethod
    async def search(
        cls, session: AsyncSession, user_filter: dict, offset: int = 0, limit: int = 20
    ):

        found = await super().find(
            session=session,
            offset=offset,
            limit=limit,
            filters=[Filter(**user_filter)],
        )
        if not found:
            raise HTTPException(status_code=404, detail="Users not found")

        return found

    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username: str):
        stmt = select(cls.model).options(joinedload(cls.model.role)).where(cls.model.username == username)  # type: ignore[arg-type]

        result = await session.exec(stmt)
        user = result.one_or_none()

        return user
