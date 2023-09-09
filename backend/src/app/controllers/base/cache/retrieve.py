from typing import Optional


class BaseCacheRetrieveController:
    """
    Base controller to retrieve a record from cache.
    """

    async def get_cache(self, key: str, field: str | None = None) -> Optional[dict]:
        """
        Get user from cache.
        """
        result = await self.repository.get_cache(key=key, field=field)
        return result
