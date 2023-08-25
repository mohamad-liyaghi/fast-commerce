from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional
from redis import Redis
from src.core.database import Base
from .cache import BaseCacheRepository


class BaseRepository(BaseCacheRepository):
    """
    Base repository class
    Methods:
        create: Create a new instance of model
        update: Update an instance of model
        delete: Delete an instance of model
        retrieve: Retrieve an instance of model
        list: List all instances of model
    """

    def __init__(self, model: Base, database: AsyncSession, redis: Redis):
        super().__init__(redis_client=redis)
        self.model = model
        self.database = database

    async def create(self, **data):
        """
        Create a new instance of model
        :param data: data to create new instance
        :return: created instance
        """
        instance = self.model(**data)
        self.database.add(instance)
        await self.database.commit()
        await self.database.refresh(instance)
        return instance

    async def update(self, instance: Base, **data):
        """
        Update an instance of model
        :param instance: instance to update
        :param data: data to update
        :return: updated instance
        """
        for key, value in data.items():
            setattr(instance, key, value)
        await self.database.commit()
        await self.database.refresh(instance)
        return instance

    async def delete(self, instance: Base):
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        self.database.delete(instance)
        await self.database.commit()

    async def retrieve(
        self,
        join_query: Optional[selectinload] = None,
        many: bool = False,
        last: bool = False,
        **kwargs
    ):
        """
        Retrieve instance(s) of model based on given filters.
        :param join_query: Join query to be used for eager loading
        :param many: Retrieve many instances if True, else single instance
        :param last: Retrieve the last instance if True (requires many=False)
        :param kwargs: Filter parameters
        :return: Instance(s)
        """
        filters = await self._make_filter(self.model, kwargs)
        query = select(self.model).where(and_(*filters))

        if join_query:
            query = query.options(join_query)

        if last:
            query = query.order_by(desc(self.model.id))

        result = await self.database.execute(query)

        if result:
            return result.scalars().all() if many else result.scalars().first()

    async def list(self, limit: int = 100, skip: int = 0, **kwargs):
        """
        List all instances of model
        :param limit: limit of instances
        :param skip: skip instances
        :param kwargs: filter parameters
        :return: list of instances
        """
        query = select(self.model).where(**kwargs).offset(skip).limit(limit)

        result = await self.database.execute(query)
        instances = result.scalars().all()
        return instances

    @staticmethod
    async def _make_filter(model, filters: dict) -> list:
        """
        Generate filters for query based on given dictionary.
        eg: {'id': 1, 'name': 'test'} -> [model.id == 1, model.name == 'test']
        :param model: SQLAlchemy model
        :param filters: Dictionary containing filter fields and values
        :return: List of filter conditions
        """
        return [getattr(model, field) == value for field, value in filters.items()]
