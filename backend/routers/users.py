from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from session import AsyncSessionLocal
from dependencies import get_session
from dao.user import UserDAO
from dao.filter import Filter
from models.user import ShowUser, CreateUser, UpdateUser, FindUser

router = APIRouter(prefix="/users", tags=["Точка работы с пользователями"])


@router.get("/", summary="Получить данные пользователей", response_model=list[ShowUser])
async def find(
    session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 20
):
    return await UserDAO.find(session=session, offset=offset, limit=limit)


@router.get(
    "/find", summary="Найти пользователя по фильтру", response_model=list[ShowUser]
)
async def find_by_filter(
    filter: Annotated[Filter, Depends()], session: AsyncSession = Depends(get_session)
):
    filter_dict = filter.model_dump(exclude_unset=True)

    return await UserDAO.search(
        session=session, user_filter=filter_dict, offset=0, limit=20
    )


@router.get(
    "/{id}", summary="Получить данные пользователя по ID", response_model=ShowUser
)
async def find_one(id: int, session: AsyncSession = Depends(get_session)):
    return await UserDAO.find_one(session=session, id=id)


@router.post("/", summary="Создание пользователя", response_model=ShowUser)
async def create_user(
    user_data: CreateUser, session: AsyncSession = Depends(get_session)
):
    return await UserDAO.create(user=user_data, session=session)


@router.patch("/{id}", summary="Обновление данных пользователя", response_model=ShowUser)
async def update_user(
    id: int, user_data: UpdateUser, session: AsyncSession = Depends(get_session)
):

    user = await UserDAO.update(id=id, data=user_data, session=session)

    if not user:
        raise HTTPException(404, "User not exists")

    return user


@router.delete("/{id}", summary="Удаление пользователя", response_model=ShowUser)
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    user = await UserDAO.delete(id=id, session=session)

    if user is None:
        raise HTTPException(404, "User not exists")

    return user
