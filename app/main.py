import logging
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.settings import settings
from app.db.database import engine
from app.db.session import MongoConnection

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")

    # Startup - инициализируем соединения
    try:
        # MongoDB соединение будет создано при первом обращении
        logger.info("Приложение запущено успешно")
        yield
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
        raise
    finally:
        # Shutdown - закрываем соединения
        logger.info("Остановка приложения...")
        await MongoConnection.close()
        await engine.dispose()
        logger.info("Приложение остановлено")


app = FastAPI(
    title="Category Service",
    description="API для поиска товаров по требованиям тендера с использованием LLM",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Category API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Простой health check для Kubernetes liveness probe"""
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level="info"
    )

