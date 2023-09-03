from typing import Any, Optional
from src.app.repositories.base import BaseRepository


class BaseCacheController:
    """
    This controller is used to interact with cache.
    Also it is parent class for BaseController.
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create_cache(self, key: str, data: dict, ttl: int = None):
        """
        Create a new record in cache.
        """
        await self.repository.create_cache(key=key, data=data, ttl=ttl)

    async def get_cache(self, key: str, field: str | None = None):
        """
        Get user from cache.
        """
        result = await self.repository.get_cache(key=key, field=field)
        return result

    async def delete_cache(self, key: str, field: Optional[Any] = None):
        """
        Delete user from cache.
        """
        await self.repository.delete_cache(key=key, field=field)
