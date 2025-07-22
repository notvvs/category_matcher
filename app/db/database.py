from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)

try:
    engine: AsyncEngine = create_async_engine(
        settings.get_postgres_dsn,
        echo=False,
    )

    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

except SQLAlchemyError as e:
    logger.error(f"Failed to create database engine: {e}")
    raise