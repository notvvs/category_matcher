import asyncio

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.session import get_db, get_mongo_db
from app.repository.mongo_repository import MongoRepo
from app.repository.postgres_repository import PostgresRepo
from app.services.llm_service import OllamaCategorizer


class Test:
    def __init__(self, postgres_session: AsyncSession, mongo_db: AsyncIOMotorDatabase, collection_name: str):
        self.llm = OllamaCategorizer()
        self.postgres = PostgresRepo(postgres_session)
        self.mongodb = MongoRepo(mongo_db, collection_name)

    async def test(self):
        products = await self.mongodb.get_all()
        print(f"Найдено продуктов: {len(products)}")

        for product in products:
            print(">>> ПРОДУКТ:", product.get("title"))
            category = product.get("yandex_category")
            print("Категория:", category)
            if category:
                children = await self.postgres.get_children(category)
                print("Дочерние категории:", children)

                res = await self.llm.categorize_product(
                    product.get("title"),
                    product.get("description"),
                    category
                )
                print("Категоризация:", res)


async def main():
    # Получаем зависимости
    async with get_db() as postgres_session:
        mongo_db = await get_mongo_db()

        # Создаем экземпляр Test
        test = Test(postgres_session, mongo_db, 'test')

        # Вызываем метод
        await test.test()

asyncio.run(main())