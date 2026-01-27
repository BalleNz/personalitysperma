from .generation_router import router as generation_router
from .auth_router import auth_router
from .characteristics_router import router as characteristics_router

__all__ = [
    "generation_router",
    "auth_router",
    "characteristics_router"
]
