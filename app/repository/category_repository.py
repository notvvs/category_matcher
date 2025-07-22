from typing import List
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from app.models.category import Category

logger = logging.getLogger(__name__)


class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_parent_categories(self) -> List[Category]:
        """Получить все родительские категории (у которых parent_id == None)"""
        try:
            stmt = select(Category).where(Category.parent_id.is_(None))
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching parent categories: {e}")
            raise

    async def get_children(self, parent_name: str) -> List[str]:
        """Получить потомков категории товара по названию родителя"""
        try:
            stmt = (
                select(Category)
                .where(Category.name == parent_name)
                .options(selectinload(Category.children))
            )
            result = await self.session.execute(stmt)
            category = result.scalar_one_or_none()

            if category is None:
                logger.warning(f"Category '{parent_name}' not found")
                return []

            return [child.name for child in category.children]
        except SQLAlchemyError as e:
            logger.error(f"Error fetching children for category '{parent_name}': {e}")
            raise