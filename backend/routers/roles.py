from fastapi import APIRouter
from dao.role import create_roles

router = APIRouter(prefix="/roles", tags=["Точка работы с ролями пользователелй"])


@router.post("/")
def make_roles():
    return {"Roles was made": create_roles()}
