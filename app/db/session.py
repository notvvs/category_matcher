from typing import AsyncGenerator
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import ConnectionFailure

from app.core.settings import settings
from app.db.database import async_session

logger = logging.getLogger(__name__)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии для ДИ"""
    try:
        async with async_session() as session:
            yield session
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        raise

async def get_mongo_db() -> AsyncIOMotorDatabase:
    """Получение базы данных MongoDB для ДИ"""
    try:
        client = AsyncIOMotorClient(settings.get_mongo_dsn)
        # Проверяем подключение
        await client.admin.command('ping')
        return client[settings.MONGO_DB_NAME]
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise