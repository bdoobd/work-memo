from fastapi import APIRouter, Query
from dao.user import add, read
from models.user import User, ShowUser, CreateUser
from auth.auth import get_password_hash

router = APIRouter(prefix="/users", tags=["Точка работы с пользователями"])


@router.post("/", response_model=ShowUser)
def create_user(user: CreateUser):

    password_hash = {"password_hash": get_password_hash(user.password)}

    db_user = User.model_validate(user, update=password_hash)

    result = add(db_user)

    return result


@router.get("/", response_model=list[ShowUser])
def fetch_all(offset: int = 0, limit: int = Query(default=20, le=20)):
    return read(offset, limit)


# @router.get("/all")
# def get_all_users():
#     return {"all users": get_all_users_dao()}


# @router.get("/get_with_roles")
# def get_users_with_roles():
#     return {"users with roles": select_users_with_roles()}


# @router.post("/create")
# def create_user():
#     create_user_dao()
#     return {"action": "Creating new user"}


# @router.put("/update")
# def update_user(id: int, password: str):
#     user = update_user_by_id(id=id, password=password)
#     return {"Updating user with ID": user}


# @router.delete("/delete")
# def remove_user(id: int):
#     return {"Removed user": delete_user(id=id)}


# @router.get("/create_user_role")
# def create_user_and_role():
#     return {"action": add_user_with_new_role()}


# @router.get("/user_role")
# def get_user_role():
#     return {"action": create_user_and_role()}


# @router.get("/users_role")
# def users_role():
#     return get_users_role()


# @router.get("/users_in_role")
# def users_in_role():
#     return get_roles_members()


# @router.get("/{name}")
# def get_user_name(name: str):
#     return {"action": select_users()}
# @router.get("/{id}")
# def get_user_data(id: int):
#     return {"action": get_user_by_id_dao(id)}
