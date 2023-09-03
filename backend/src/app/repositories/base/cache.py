from redis import Redis


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
        if ttl:
            await self.client.expire(key, ttl)

    async def get_cache(self, key: str, field: str | None = None):
        """
        Get user from cache.
        """
        if field:
            result = await self.client.hget(key, field)
        else:
            result = await self.client.hgetall(key)
        return result

    async def delete_cache(self, key: str, field: str | None = None):
        """
        Delete user from cache.
        """
        if field:
            await self.client.hdel(key, field)
        else:
            await self.client.delete(key)
