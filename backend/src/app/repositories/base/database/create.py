from typing import List
from src.core.database import Base


class BaseCreateRepository:
    """
    This repository is responsible for all the create operations.
    """

    async def create(self, **data: dict) -> Base:
        """
        Create a new instance of model
        """
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def bulk_create(self, instances: List[Base]) -> List[Base]:
        """
        Create a new instance of model
        :param instances: data to create new instance
        :return: created instance
        """
        self.session.add_all(instances)
        await self.session.commit()
        return instances
