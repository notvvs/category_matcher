from app.repository.mongo_repository import MongoRepo
from app.repository.postgres_repository import PostgresRepo
from app.services.llm_service import OllamaCategorizer


class MatchService:
    def __init__(self):
        self.llm = OllamaCategorizer()
        self.postgres = PostgresRepo()
        self.mongodb = MongoRepo()