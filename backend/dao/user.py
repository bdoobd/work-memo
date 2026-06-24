from sqlmodel.ext.asyncio.session import AsyncSession

from .base import BaseDAO
from models.user import CreateUser, User, WriteUser
from auth.auth import get_password_hash
from dao.filter import Filter


class UserDAO(BaseDAO[User]):

    model = User

    @classmethod
    async def create(cls, user: CreateUser, session: AsyncSession) -> WriteUser:
        if not user.password == user.password_confirm:
            raise Exception("Passwords do not match")

        values = user.model_dump(exclude_unset=True)
        values["password_hash"] = get_password_hash(user.password)

        return await super().create(data=WriteUser(**values), session=session)

        # return result

    @classmethod
    async def search(
        cls, session: AsyncSession, user_filter: dict, offset: int = 0, limit: int = 20
    ):

        return await super().find(
            session=session,
            offset=offset,
            limit=limit,
            filters=[Filter(**user_filter)],
        )
