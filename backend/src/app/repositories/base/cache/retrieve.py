class BaseCacheRetrieveRepository:
    """
    Base repository to retrieve a record from cache.
    """

    async def get_cache(self, key: str, field: str | None = None):
        """
        Get a record from cache.
        Args:
            key: key to retrieve
            field: field to retrieve
        """
        if field:
            result = await self.client.hget(key, field)
        else:
            result = await self.client.hgetall(key)
        return result
