from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId

class MongoRepository:
    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str):
        self.collection: AsyncIOMotorCollection = database[collection_name]

    async def add(self, data: Dict[str, Any]) -> str:
        """Добавить документ"""
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        """Обновить документ"""
        if not ObjectId.is_valid(id):
            return False

        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        return result.modified_count > 0

    async def get_all(self, limit: Optional[int] = None, skip: int = 0) -> List[Dict[str, Any]]:
        """Получить все документы с опциональной пагинацией"""
        cursor = self.collection.find().skip(skip)

        if limit:
            cursor = cursor.limit(limit)

        documents = await cursor.to_list(length=limit)

        for doc in documents:
            doc["_id"] = str(doc["_id"])

        return documents