from redis.asyncio.client import Redis
from .base import redis_pool


async def get_redis() -> Redis:
    """
    Return a Redis instance
    """
    redis = Redis(connection_pool=redis_pool)
    return redis
