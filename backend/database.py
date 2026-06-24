import config
from functools import lru_cache
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine


@lru_cache()
def get_settings():
    return config.Settings()


engine = create_async_engine(get_settings().db_url(), echo=get_settings().DEBUG)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
