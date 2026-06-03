from typing import TypeVar, Generic, Type
from sqlmodel import SQLModel, Session, select
from .filter import Filter
from .expression_builder import builder
from database import engine

T = TypeVar("T")


class BaseDAO(Generic[T]):

    model: Type[T]

    @classmethod
    def find(cls, offset: int, limit: int, filters: list[Filter] | None = None):

        query = select(cls.model)

        if filters:
            expressions = [builder(cls.model, filter_) for filter_ in filters]

            query = query.where(*expressions)

        with Session(engine) as session:
            result = session.exec(query.offset(offset=offset).limit(limit=limit)).all()

        return result

    @classmethod
    def find_one(cls, id: int):
        with Session(engine) as session:
            result = session.get(cls.model, id)

        return result

    @classmethod
    def create(cls, data: SQLModel):
        values = data.model_dump(exclude_unset=True)
        instance = cls.model(**values)
        with Session(engine) as session:
            session.add(instance=instance)
            session.commit()
            session.refresh(instance=instance)

        return instance

    @classmethod
    def update(cls, id: int, data: SQLModel):

        with Session(engine) as session:
            found = session.get(cls.model, id)

            if not found:
                return None

            updates = data.model_dump(exclude_unset=True)

            for key, value in updates.items():
                setattr(found, key, value)

            session.add(found)
            session.commit()
            session.refresh(found)

            return found
