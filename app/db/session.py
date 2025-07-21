from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии для ДИ"""
    async with async_session() as session:
        yield session
