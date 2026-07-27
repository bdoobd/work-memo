from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies import get_session
from dao.role import RoleDAO
from models.role import ShowRole, UpdateRole

router = APIRouter(prefix="/roles", tags=["Точка работы с ролями пользователелй"])


@router.get("/", summary="Получить все роли пользователей", response_model=list[ShowRole])
async def get_all(session: AsyncSession = Depends(get_session)):
    return await RoleDAO.find(session=session, offset=0, limit=20)


@router.post("/", summary="Создать роли пользователей", response_model=ShowRole)
async def make_roles(data: UpdateRole, session: AsyncSession = Depends(get_session)):
    return await RoleDAO.create(data=data, session=session)

@router.patch("/{id}", summary="Обновить роль пользователя", response_model=ShowRole)
async def update_role(id: int, data: UpdateRole, session: AsyncSession = Depends(get_session)):
    return await RoleDAO.update(id=id, data=data, session=session)  

@router.delete("/{id}", summary="Удалить роль пользователя", response_model=ShowRole)
async def delete_role(id: int, session: AsyncSession = Depends(get_session)):
    return await RoleDAO.delete(id=id, session=session)  