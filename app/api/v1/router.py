from fastapi import APIRouter

from app.api.v1.endpoints import category_routes

api_router = APIRouter()

# Подключаем роутеры
api_router.include_router(
    category_routes.router,
    prefix="/category",
    tags=["category"]
)