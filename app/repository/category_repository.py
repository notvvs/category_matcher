import asyncio
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.tables import category_table  # Таблица с колонками


class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_parents(self) -> List[str]:
        # Запрос для получения родительских категорий
        stmt = select(category_table).where(category_table.c.parent_id == None)
        result = await self.session.execute(stmt)
        return result.fetchall()
