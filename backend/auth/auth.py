# from datetime import datetime, timezone, timedelta

# from pwdlib import PasswordHash
from sqlmodel.ext.asyncio.session import AsyncSession

# import jwt

# from config import settings
from auth.security import verify_password
from dao.user import UserDAO

# pwh = PasswordHash.recommended()


# def get_password_hash(password: str) -> str:
#     return pwh.hash(password)


# def verify_password(plain_password: str, password_hash: str) -> bool:
#     return pwh.verify(plain_password, password_hash)


async def authenticate_user(username: str, password: str, session: AsyncSession):

    DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$B8c70agyFZP5B8GXs0/+yg$rmBCtk2yxRuzOXXZIIkcs2ntN5zeQeQh2Lv65Wyo+1U"
    user = await UserDAO.get_user_by_username(session=session, username=username)

    if not user:
        # HACK: Проверка пароля против статичного хеша для выравнивания времени срабатывания
        # ответа от сервера при не верном имени пользователя для предотвращения атак
        # путём подбора имени пользователя по времени ответа сервера
        verify_password(plain_password=password, password_hash=DUMMY_HASH)
        return False

    if not verify_password(plain_password=password, password_hash=user.password_hash):
        return False

    return user


# def create_token(data: dict, expires_delta: timedelta | None = None):
#     tmp_data = data.copy()

#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)

#     tmp_data.update({"exp": expire})

#     token = jwt.encode(tmp_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#     return token
