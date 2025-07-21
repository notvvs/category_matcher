from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.database import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии для ДИ"""
    async with async_session() as session:
        yield session

async def get_mongo_db() -> AsyncIOMotorDatabase:
    """Получение базы данных MongoDB для ДИ"""
    client = AsyncIOMotorClient(settings.get_mongo_connection_string)
    return client[settings.MONGO_DB_NAME]