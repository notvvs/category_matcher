from typing import List, Dict, Any, Optional
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)

class MongoRepository:
    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str):
        self.collection: AsyncIOMotorCollection = database[collection_name]

    async def add(self, data: Dict[str, Any]) -> str:
        """Добавить документ"""
        try:
            result = await self.collection.insert_one(data)
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error adding document: {e}")
            raise

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        """Обновить документ"""
        if not ObjectId.is_valid(id):
            logger.warning(f"Invalid ObjectId: {id}")
            return False

        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            logger.error(f"Error updating document {id}: {e}")
            raise

    async def get_all(self, limit: Optional[int] = None, skip: int = 0) -> List[Dict[str, Any]]:
        """Получить все документы с опциональной пагинацией"""
        try:
            cursor = self.collection.find().skip(skip)

            if limit:
                cursor = cursor.limit(limit)

            documents = await cursor.to_list(length=limit)

            for doc in documents:
                doc["_id"] = str(doc["_id"])

            return documents
        except PyMongoError as e:
            logger.error(f"Error fetching documents: {e}")
            raise