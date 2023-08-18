from redis.asyncio import ConnectionPool
from src.core.config import settings

# Redis connection pool
redis_pool = ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=100,
    decode_responses=True
)
