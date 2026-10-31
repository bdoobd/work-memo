from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db

from routers.items import router as item_router
from routers.users import router as user_router
from routers.roles import router as role_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan, title="Template for REST API")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

# @app.get("/")
# async def get_root():
#     """Удалить этот эндпойнт после тестов

#     Returns:
#         _type_: none
#     """
#     async with AsyncSessionLocal() as session:
#         print(type(session))

#     return {"message": "Root Endpoint"}


app.include_router(user_router)
app.include_router(item_router)
app.include_router(role_router)
