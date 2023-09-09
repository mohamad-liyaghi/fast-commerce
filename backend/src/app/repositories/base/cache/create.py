class BaseCacheCreateRepository:
    """
    Base repository to create a new record in cache.
    """

    async def create_cache(self, key: str, data: dict, ttl: int = None) -> None:
        """
        Create a new record in cache.
        """
        await self.client.hset(key, mapping=data)
        if ttl:
            await self.client.expire(key, ttl)
