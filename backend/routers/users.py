from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from dao.user import UserDAO
from dao.filter import Filter
from models.user import ShowUser, CreateUser, UpdateUser, FindUser

router = APIRouter(prefix="/users", tags=["Точка работы с пользователями"])


@router.get(
    "/",
    summary="Получить данные пользователей (всех или по фильтру)",
    response_model=list[ShowUser],
)
def find(offset: int = 0, limit: int = 20):

    return UserDAO.find(offset=offset, limit=limit)


@router.get(
    "/find", summary="Найти пользователя по фильтру", response_model=list[ShowUser]
)
def find_by_filter(filter: Annotated[Filter, Depends()]):
    filter_dict = filter.model_dump(exclude_unset=True)

    return UserDAO.search(user_filter=filter_dict)


@router.get("/{id}", summary="Найти пользователя по ID", response_model=ShowUser)
def find_by_id(id: int):
    user = UserDAO.find_one(id=id)

    if not user:
        raise HTTPException(404, "user not found")

    return user


@router.post("/", summary="Создание пользователя")
def create_user(user_data: CreateUser):
    user = UserDAO.create(user=user_data)

    return user


@router.patch("/{id}", summary="Обновление данных пользователя")
def update_user(id: int, user_data: UpdateUser):
    user = UserDAO.update(id=id, data=user_data)
    if not user:
        raise HTTPException(404, "Can't update not existing user")

    return user


@router.delete("/{id}", summary="Удаление пользователя", response_model=ShowUser)
def delete_user(id: int):
    return {"Deleting user data": id}
