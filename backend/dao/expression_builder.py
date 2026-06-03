from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import case
from dao.filter import Filter


def builder(model, filter_: Filter) -> ColumnElement:
    column = getattr(model, filter_.field)

    match filter_.operator:
        case "eq":
            return column == filter_.value
        case "ne":
            return column != filter_.value
        case "gt":
            return column > filter_.value
        case "lt":
            return column < filter_.value
        case "gte":
            return column >= filter_.value
        case "lte":
            return column <= filter_.value
        case "in":
            return column.in_(filter_.value)
        case "like":
            return column.like(filter_.value)
        case "not_in":
            return ~column.in_(filter_.value)
        case "between":
            return column.between(filter_.value[0], filter_.value[1])
        case "is_null":
            return column.is_(None)
        case "is_not_null":
            return column.is_not(None)
        case _:
            raise ValueError(f"Unsupported operator: {filter_.operator}")
