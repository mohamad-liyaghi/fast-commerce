from typing import Any, Optional


class BaseCacheDeleteController:
    """
    Base controller to delete a record in cache.
    """

    async def delete_cache(self, key: str, field: Optional[Any] = None) -> None:
        """
        Delete a record from cache.
        """
        await self.repository.delete_cache(key=key, field=field)
