from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError

from session import AsyncSessionLocal
from config import settings
from schemas.token import TokenData
from schemas.user import ShowUser
from exceptions import IncorrectCredentials
from dao.user import UserDAO
from database import engine

oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise


async def get_current_user(
    token: Annotated[str, Depends(oauth2)], session: AsyncSession = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get("username")

        if username is None:
            raise IncorrectCredentials

        userdata = TokenData(**payload)
    except InvalidTokenError:
        raise IncorrectCredentials

    user = await UserDAO.find_one(session=session, id=userdata.id)

    print(user)

    if user is None:
        raise IncorrectCredentials

    return user


async def get_current_active_user(
    current_user: Annotated[ShowUser, Depends(get_current_user)],
):

    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return current_user


async def is_admin(current_user: Annotated[ShowUser, Depends(get_current_user)]):
    if current_user.role.role != "admin" or current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have right privileges",
        )

    return current_user


async def is_power(current_user: Annotated[ShowUser, Depends(get_current_user)]):
    if (
        current_user.role.role != "admin" and current_user.role.role != "power"
    ) or current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have right privileges",
        )

    return current_user
