from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from session import AsyncSessionLocal


def connection(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
