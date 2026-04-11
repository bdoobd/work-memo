from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    # Указал значения по умолчанию для всех переменных, чтобы не было ошибки при запуске без .env файла
    DB_USER: str = 'nobody'
    DB_PASSWORD: str = 'nobody'
    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'nobody'
    SECRET_KEY: str = 'nobody'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = False

    def db_url(self) -> str:
        """Генерирует URL для подключения к базе данных

        Returns:
            str: URL для подключения к базе данных
        """
        # return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
