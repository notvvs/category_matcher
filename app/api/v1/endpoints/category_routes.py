import logging

from fastapi import APIRouter
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, get_mongo_db
from app.services.category_service import CategoryService

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post('/process_category')
async def process_category(collection_name: str,
                           postgres_session: AsyncSession = Depends(get_db),
                           mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    service = CategoryService(postgres_session, mongo_db, collection_name)
    await service.match_category()
    return {"status": "processed"}