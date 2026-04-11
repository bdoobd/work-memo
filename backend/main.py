from fastapi import FastAPI
from models.user import SQLModel
from routers.items import router as item_router
from routers.users import router as user_router
from routers.roles import router as role_router
from database import engine


app = FastAPI()


@app.get("/")
async def get_root() -> dict:
    """Удалить этот эндпойнт после тестов

    Returns:
        _type_: none
    """
    create_db_and_tables()

    return {"message": "Root endpoint"}


app.include_router(user_router)
app.include_router(item_router)
app.include_router(role_router)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
