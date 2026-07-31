from sqlalchemy.exc import SQLAlchemyError

from session import AsyncSessionLocal


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
