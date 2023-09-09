class BaseCacheCreateController:
    """
    Base controller to create a new record in cache.
    """

    async def create_cache(self, key: str, data: dict, ttl: int = None) -> None:
        """
        Create a new record in cache.
        """
        await self.repository.create_cache(key=key, data=data, ttl=ttl)
