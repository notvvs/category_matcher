from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Настройка подключения к Postgres
    PG_HOST: str = 'localhost'
    PG_USER: str = 'postgres'
    PG_PASS: str = '1202'
    PG_PORT: int = 5432
    PG_DB_NAME: str = 'postgres'

    # Настройка подключения к MongoDB
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017

    # Получение ссылки для подключения к Postgres
    @property
    def get_postgres_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}'

    @property
    def get_mongo_dsn(self) -> str:
        return f'mongodb://{self.MONGO_HOST}"{self.MONGO_PORT}'

    class Config:
        env_file = ".env"

settings = Settings()