import config
from functools import lru_cache
from sqlmodel import create_engine


@lru_cache()
def get_settings():
    return config.Settings()


engine = create_engine(get_settings().db_url(), echo=get_settings().DEBUG)
