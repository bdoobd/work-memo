from fastapi import APIRouter
from dao.user import (
    create_user as create_user_dao,
    get_all_users as get_all_users_dao,
    get_user_by_id as get_user_by_id_dao,
    get_user_by_name,
    update_user_by_id,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Точка работы с пользователями"])


@router.get("/all")
def get_all_users():
    return {"all users": get_all_users_dao()}


@router.get("/test")
def by_name():
    return {"by name": get_user_by_name()}


@router.post("/create")
def create_user():
    create_user_dao()
    return {"action": "Creating new user"}


@router.put("/update")
def update_user(id: int, password: str):
    user = update_user_by_id(id=id, password=password)
    return {"Updating user with ID": user}


@router.delete("/delete")
def remove_user(id: int):
    return {"Removed user": delete_user(id=id)}


@router.get("/{id}")
def get_user_data(id: int):
    return {"action": get_user_by_id_dao(id)}
#
