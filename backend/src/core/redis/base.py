from redis.asyncio import ConnectionPool
from core.config import settings

# Redis connection pool
redis_pool = ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=100,
)
