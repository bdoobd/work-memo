from .base import BaseDAO
from models.user import CreateUser, User, WriteUser
from auth.auth import get_password_hash
from dao.filter import Filter


class UserDAO(BaseDAO[User]):

    model = User

    @classmethod
    def create(cls, user: CreateUser) -> WriteUser:
        if not user.password == user.password_confirm:
            raise Exception("Passwords do not match")

        values = user.model_dump(exclude_unset=True)
        values["password_hash"] = get_password_hash(user.password)

        result = super().create(WriteUser(**values))

        return result

    @classmethod
    def search(cls, user_filter: dict, offset: int = 0, limit: int = 20):

        return super().find(
            offset=offset,
            limit=limit,
            filters=[Filter(**user_filter)],
        )
