import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.mongo_repository import MongoRepo
from app.repository.postgres_repository import PostgresRepo
from app.services.llm_service import OllamaCategorizer

logger = logging.getLogger(__name__)

class CategoryService:
    def __init__(self, postgres_session: AsyncSession, mongo_db: AsyncIOMotorDatabase, collection_name: str):
        self.llm = OllamaCategorizer()
        self.postgres = PostgresRepo(postgres_session)
        self.mongodb = MongoRepo(mongo_db, collection_name)

    async def categorize_recursively(self, product_title: str, product_description: str, current_category: str) -> str:
        children = await self.postgres.get_children(current_category)

        if not children:
            return current_category

        selected_category = await self.llm.categorize_product(
            product_title,
            product_description,
            children
        )

        if not selected_category or selected_category not in children:
            return current_category

        return await self.categorize_recursively(product_title, product_description, selected_category)

    async def get_first_level_categories(self):
        """Получает категории первого уровня (дочерние от родительских, кроме Электроники)"""
        parents = []
        null_categories = await self.postgres.get_parent_categories()
        for parent in null_categories:
            if parent.name == 'Электроника':
                continue
            parents.extend(await self.postgres.get_children(parent.name))
        return parents

    async def match_category(self):
        products = await self.mongodb.get_all()

        for product in products:
            logger.info(f"Товар: {product.get("title")}")
            category = product.get("yandex_category")

            if category:
                # Если у товара есть категория - используем рекурсивную категоризацию
                final_category = await self.categorize_recursively(
                    product.get("title"),
                    product.get("description"),
                    category
                )
                logger.info(f"Финальная категория: {final_category}")
            else:
                # Если категории нет - начинаем с первого уровня
                first_level_categories = await self.get_first_level_categories()

                if first_level_categories:
                    selected_category = await self.llm.categorize_product(
                        product.get("title"),
                        product.get("description"),
                        first_level_categories
                    )

                    if selected_category:
                        final_category = await self.categorize_recursively(
                            product.get("title"),
                            product.get("description"),
                            selected_category
                        )
                        logger.info(f"Финальная категория: {final_category}")
                    else:
                        logger.error('Не удалось получить категорию')