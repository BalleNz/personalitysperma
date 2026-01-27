from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.app.main import fastapi_app
from src.infrastructure.config.config import config
from src.infrastructure.config.loggerConfig import configure_logging
from src.infrastructure.database.engine import clear_metadata_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: очистка кеша метаданных при запуске
    await clear_metadata_cache()
    print("✓ Metadata cache cleared")

    yield  # Здесь приложение работает

    # Shutdown (опционально)
    print("Application shutting down")

app = fastapi_app
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    configure_logging()
    uvicorn.run(
        app=fastapi_app,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )
