from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.repository.mongo_repository import MongoRepo
from app.repository.postgres_repository import PostgresRepo
from app.services.llm_service import OllamaCategorizer


class CategoryService:
    def __init__(self, postgres_session: AsyncSession, mongo_db: AsyncIOMotorDatabase, collection_name):
        self.llm = OllamaCategorizer()
        self.postgres = PostgresRepo(postgres_session)
        self.mongodb = MongoRepo(mongo_db, collection_name)