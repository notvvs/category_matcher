from contextlib import asynccontextmanager
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

class MongoConnection:
    _client = None
    _database = None

    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase:
        if cls._client is None:
            try:
                cls._client = AsyncIOMotorClient(settings.get_mongo_dsn)
                # Проверяем подключение
                await cls._client.admin.command('ping')
                cls._database = cls._client[settings.MONGO_DB_NAME]
                logger.info("MongoDB connection established")
            except ConnectionFailure as e:
                logger.error(f"MongoDB connection failed: {e}")
                raise
        return cls._database

    @classmethod
    async def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._database = None
            logger.info("MongoDB connection closed")

async def get_mongo_db() -> AsyncIOMotorDatabase:
    """Получение базы данных MongoDB для ДИ"""
    return await MongoConnection.get_database()