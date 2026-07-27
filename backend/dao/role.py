from .base import BaseDAO
from models.role import Role


class RoleDAO(BaseDAO[Role]):
    model = Role
