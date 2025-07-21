from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Настройка подключения к Postgres
    PG_HOST: str = 'localhost'
    PG_USER: str = 'postgres'
    PG_PASS: str = '1202'
    PG_PORT: int = 5432
    PG_DB_NAME: str = 'postgres'

    # Получение ссылки для подключения к Postgres
    @property
    def get_postgres_connection_link(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}'

    class Config:
        env_file = ".env"

settings = Settings()