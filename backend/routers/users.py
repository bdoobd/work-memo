from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from dao.session_builder import get_session
from dependencies import get_current_active_user, is_admin
from services.user import UserService
from dao.user import UserDAO
from dao.filter import Filter
from schemas.user import ShowUser, User, CreateUser, UpdateUserPassowrds
from schemas.token import Token
from auth.auth import authenticate_user
from exceptions import IncorrectCredentials

router = APIRouter(prefix="/users", tags=["Точка работы с пользователями"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.get("/", summary="Получить данные пользователей", response_model=list[ShowUser])
async def find(
    session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 20
):
    return await UserDAO.find(session=session, offset=offset, limit=limit)


@router.get("/find", summary="Найти пользователя по фильтру", response_model=list[User])
async def find_by_filter(
    filter: Annotated[Filter, Depends()], session: AsyncSession = Depends(get_session)
):
    filter_dict = filter.model_dump(exclude_unset=True)

    return await UserDAO.search(
        session=session, user_filter=filter_dict, offset=0, limit=20
    )


@router.get("/me", summary="Данные профилья пользователя", response_model=ShowUser)
async def show_me(current_user: Annotated[ShowUser, Depends(get_current_active_user)]):

    active = await get_current_active_user(current_user=current_user)

    return active


@router.get(
    "/{id}", summary="Получить данные пользователя по ID", response_model=ShowUser
)
async def find_one(id: int, session: AsyncSession = Depends(get_session)):
    return await UserDAO.find_one(session=session, id=id)


@router.post("/", summary="Создание пользователя", response_model=User)
async def create_user(
    user_data: CreateUser, session: AsyncSession = Depends(get_session)
):
    user = await UserService.create_user(user_data=user_data, session=session)

    return user


@router.post("/login", summary="Выполнить вход пользователя", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise IncorrectCredentials()

    return UserService.create_token(user.model_dump())


@router.patch("/{id}", summary="Обновление данных пользователя")
async def update_user(
    id: int,
    user_data: UpdateUserPassowrds,
    session: AsyncSession = Depends(get_session),
):

    user = await UserService.update(id=id, data=user_data, session=session)

    return user


@router.delete("/{id}", summary="Удаление пользователя", response_model=User)
async def delete_user(
    admin: Annotated[ShowUser, Depends(is_admin)],
    id: int,
    session: AsyncSession = Depends(get_session),
):
    user = await UserDAO.delete(id=id, session=session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
