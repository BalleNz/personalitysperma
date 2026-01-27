from fastapi import FastAPI

from src.api.O2AuthSchema import jwt_openapi
from src.api.routers import auth_router
from src.api.routers import generation_router
from src.api.routers import characteristics_router


def get_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="DrugSearch API",
        lifespan=None
    )

    # routers
    app.include_router(generation_router, prefix="/v1", tags=["Generation"])
    app.include_router(auth_router, prefix="/v1", tags=["Auth"])
    app.include_router(characteristics_router, prefix="/v1", tags=["Characteristic"])

    # custom auth schema after including routers
    app.openapi = lambda: jwt_openapi(app)

    return app


fastapi_app: FastAPI = get_app()
