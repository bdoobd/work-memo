from fastapi import APIRouter
from dao.role import create_roles

router = APIRouter(prefix="/roles", tags=["Роли пользователелй"])


@router.post("/all")
def make_roles():
    return {"Roles was made": create_roles()}
