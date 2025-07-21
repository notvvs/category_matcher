from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.category import Category


class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_parent_categories(self) -> List[Category]:
        """Получить все родительские категории (у которых parent_id == None)"""
        stmt = select(Category).where(Category.parent_id.is_(None))
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_children(self, parent_name: str) -> List[str]:
        """Получить потомков категории товара по названию родителя"""
        stmt = (
            select(Category)
            .where(Category.name == parent_name)
            .options(selectinload(Category.children))
        )
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        names = [category.name for category in category.children]
        return names