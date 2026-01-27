from redis.asyncio import Redis

from src.core.services.cache_services.redis_service import RedisService
from src.infrastructure.config.redis_config import REDIS_POOL

redis_client = Redis(connection_pool=REDIS_POOL)

redis_service = RedisService(
    redis_client=redis_client
)


def get_redis_service() -> RedisService:
    return redis_service
