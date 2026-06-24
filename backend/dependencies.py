from session import AsyncSessionLocal

from database import engine

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session