from .main_router import router as generation_router
from .auth_router import auth_router
from .characteristics_router import router as characteristics_router
from .user_router import router as user_router
from .testing import router as test_router
from .typification import router as typification_router

__all__ = [
    "generation_router",
    "auth_router",
    "characteristics_router",
    "user_router",
    "test_router",
    "typification_router"
]
