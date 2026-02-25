from fastapi import FastAPI

from src.infrastructure.config.loggerConfig import configure_logging

configure_logging()

from src.api.O2AuthSchema import jwt_openapi
from src.api.routers import auth_router
from src.api.routers import generation_router
from src.api.routers import characteristics_router
from src.api.routers import user_router
from src.api.routers import test_router


def get_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="zaloopa API",
        lifespan=None
    )

    # routers
    app.include_router(generation_router, prefix="/v1", tags=["Generation"])
    app.include_router(auth_router, prefix="/v1", tags=["Auth"])
    app.include_router(characteristics_router, prefix="/v1", tags=["Characteristic"])
    app.include_router(user_router, prefix="/v1", tags=["User"])
    app.include_router(test_router, prefix="/v1", tags=["Testing"])

    # custom auth schema after including routers
    app.openapi = lambda: jwt_openapi(app)

    return app


fastapi_app: FastAPI = get_app()
