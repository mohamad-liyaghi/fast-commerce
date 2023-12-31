from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis
from src.core.configs import settings
from src.core.redis import get_redis
from src.main import app


async def override_get_redis() -> Redis:
    """
    Return a Redis instance [TEST]
    """
    # Redis connection pool
    redis_pool = ConnectionPool.from_url(
        settings.TEST_REDIS_URL, max_connections=100, decode_responses=True
    )
    redis = Redis(connection_pool=redis_pool)
    # Override the get_redis function
    app.dependency_overrides[get_redis] = override_get_redis
    return redis
