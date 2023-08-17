from redis import Redis
from src.core.database import Base


class BaseCacheRepository:
    """
    This repository is responsible for all the cache operations
    """
    def __init__(self, redis_client: Redis):
        self.client = redis_client

    async def create_cache(self, key: str, data: dict, ttl: int = None):
        """
        Create a new record in cache.
        """
        await self.client.hset(key, mapping=data)
        await self.client.expire(key, ttl)

    async def get_cache(self, key: str, field: str):
        """
        Get user from cache.
        """
        result = await self.client.hget(key, field)
        return result

    async def delete_cache(self, key: str):
        """
        Delete user from cache.
        """
        await self.client.hdel(key)
