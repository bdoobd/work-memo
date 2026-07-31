from datetime import timedelta

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from schemas.user import CreateUser, AddUser, UpdateUserPassowrds, UpdateUserHash
from exceptions import PasswordsDoNotMatch
from auth.security import get_password_hash
from config import settings
from auth.jwt import create_token
from schemas.token import Token
from dao.user import UserDAO
from schemas.user import TokenUser


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

    @staticmethod
    def create_token(user: dict) -> Token:

        token = TokenUser(**user)
        expires_in = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_token(data=token.model_dump(), expires_delta=expires_in)

        return Token(access_token=token, token_type="bearer")

    @staticmethod
    async def update(id: int, data: UpdateUserPassowrds, session: AsyncSession):
        if data.password is not None:
            if data.password != data.password_confirm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passwords do not match",
                )

        user_dict = data.model_dump(exclude_unset=True)

        if data.password is not None:
            user_dict["password_hash"] = get_password_hash(password=data.password)

        updates = UpdateUserHash(**user_dict)

        updated = await UserDAO.update(id=id, data=updates, session=session)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Can't update. User not exists",
            )

        return updated
