import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, get_mongo_db
from app.schemas.api import ProcessCategoryResponse
from app.services.category_service import CategoryService

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post('/process_category')
async def process_category(collection_name: str,
                           postgres_session: AsyncSession = Depends(get_db),
                           mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> ProcessCategoryResponse:
    try:
        logger.info(f"Начинаем обработку коллекции: {collection_name}")

        service = CategoryService(postgres_session, mongo_db, collection_name)
        processed_count = await service.match_category()

        logger.info(f"Обработка завершена. Обработано товаров: {processed_count}")

        return ProcessCategoryResponse(
            status="success",
            message=f"Обработка коллекции '{collection_name}' завершена успешно",
            processed_count=processed_count
        )

    except ValueError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации: {str(e)}"
        )
    except ConnectionError as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ошибка подключения к базе данных"
        )
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )