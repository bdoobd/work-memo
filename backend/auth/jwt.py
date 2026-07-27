from datetime import timedelta, datetime, timezone

import jwt

from config import settings


def create_token(data: dict, expires_delta: timedelta | None = None):
    tmp_data = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    tmp_data.update({"exp": expire})

    token = jwt.encode(tmp_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token
