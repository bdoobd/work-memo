from sqlmodel.ext.asyncio.session import AsyncSession

from auth.security import verify_password
from dao.user import UserDAO


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
