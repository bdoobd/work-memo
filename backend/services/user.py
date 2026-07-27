from sqlmodel.ext.asyncio.session import AsyncSession

from schemas.user import CreateUser, AddUser
from exceptions import PasswordsDoNotMatch
from auth.security import get_password_hash
from dao.session_builder import connection
from dao.user import UserDAO


class UserService:

    @staticmethod
    async def create_user(user_data: CreateUser, session: AsyncSession):

        if user_data.password != user_data.password_confirm:
            raise PasswordsDoNotMatch()

        hashed_password = get_password_hash(password=user_data.password)

        user_dict = user_data.model_dump()
        user_dict["password_hash"] = hashed_password

        new_user = AddUser(**user_dict)

        return await UserDAO.create(data=new_user, session=session)
