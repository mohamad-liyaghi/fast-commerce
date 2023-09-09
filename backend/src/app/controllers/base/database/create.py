from typing import List
from src.core.database import Base


class BaseCreateController:
    """
    Base class for handling create operations in db controller
    """

    async def create(self, **data) -> Base:
        """
        Create a new instance of model
        :param data: data to create new instance
        :return: created instance
        """
        result = await self.repository.create(**data)
        return result

    async def bulk_create(self, instances: List[Base]) -> List[Base]:
        """
        Create a new instance of model
        :param instances: data to create new instance
        :return: created instance
        """
        result = await self.repository.bulk_create(instances)
        return result
