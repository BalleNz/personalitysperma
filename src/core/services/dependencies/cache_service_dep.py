from src.core.services.dependencies.api_client_dep import get_api_client
from src.core.services.dependencies.redis_service_dep import get_redis_service
from src.core.services.cache_services.cache_service import CacheService

cache_service = CacheService(
    redis_service=get_redis_service(),
    api_client=get_api_client()
)


async def get_cache_service() -> CacheService:
    """Возвращает синглтон объект"""
    return cache_service
