from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from app.core.settings import settings

engine: AsyncEngine = create_async_engine(
    settings.get_postgres_connection_link,
    echo=False,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

