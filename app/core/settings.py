from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    pg_url: str = "postgresql+asyncpg://vvs:1202@localhost/categories"

    class Config:
        env_file = ".env"

settings = Settings()