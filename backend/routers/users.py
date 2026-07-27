from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies import get_session, get_current_active_user
from services.user import UserService
from dao.user import UserDAO
from dao.filter import Filter
from schemas.user import ShowUser, User, CreateUser, UpdateUser
from schemas.token import Token
from config import settings
from auth.auth import authenticate_user
from auth.jwt import create_token
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

    data = {"username": user.username, "id": user.id, "role": user.role.role}
    expires_in = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_token(data=data, expires_delta=expires_in)

    return Token(access_token=token, token_type="bearer")


# TODO: При изменении пароля требуется сверить оба указанных пароля и в случае их схожести хешировать пароль. Запись изменений через базовый метод не умеет сравнивать пароли и хешировать их. Надо создать метод в UserDAO для этого
@router.patch("/{id}", summary="Обновление данных пользователя")
async def update_user(
    id: int, user_data: UpdateUser, session: AsyncSession = Depends(get_session)
):
    print(user_data)
    print(type(user_data))
    if user_data.password is not None:
        if user_data.password != user_data.password_confirm:
            # TODO: Сделать исключение для этого типа ошибки
            raise Exception("Passwords do not match")

    user = await UserDAO.update(id=id, data=user_data, session=session)

    if not user:
        raise HTTPException(404, "User not exists")

    return user


@router.delete("/{id}", summary="Удаление пользователя", response_model=User)
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    user = await UserDAO.delete(id=id, session=session)

    if user is None:
        raise HTTPException(404, "User not exists")

    return user
