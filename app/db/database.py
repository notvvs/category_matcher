from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base
from app.core.settings import settings

Base = declarative_base()

engine: AsyncEngine = create_async_engine(
    settings.pg_url,
    echo=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

