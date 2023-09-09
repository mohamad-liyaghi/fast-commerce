class BaseCacheDeleteRepository:
    """
    Base repository to delete a record in cache.
    """

    async def delete_cache(self, key: str, field: str | None = None):
        """
        Delete a record from cache.
        """
        if field:
            await self.client.hdel(key, field)
        else:
            await self.client.delete(key)
