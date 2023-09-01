from sqlalchemy import or_, desc, select, asc, cast, String, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional
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
        self.database = database  # Database session

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
        await self.database.delete(instance)
        await self.database.commit()

    async def retrieve(
        self,
        join_fields: Optional[List[str]] = None,
        order_by: Optional[list] = None,
        many: bool = False,
        descending: bool = False,
        contains: bool = False,
        limit: int = 100,
        skip: int = 0,
        **kwargs,
    ):
        """
        Retrieve instance(s) of model based on given filters.
        """
        query = await self._make_query(
            join_fields=join_fields,
            contains=contains,
            order_by=order_by,
            descending=descending,
            limit=limit,
            skip=skip,
            **kwargs,
        )

        return await self._execute_query(session=self.database, query=query, many=many)

    async def _make_query(
        self,
        join_fields: Optional[List[str]] = None,
        order_by: Optional[list] = None,
        descending: bool = False,
        limit: int = 100,
        skip: int = 0,
        contains: bool = False,
        **kwargs,
    ):
        query = await self._make_filter(self.model, kwargs, contains)
        query = await self._make_joins(self.model, query, join_fields)
        query = await self._create_order_by(
            self.model, query, order_by, descending=descending
        )
        return query.offset(skip).limit(limit)

    @staticmethod
    async def _execute_query(session, query, many: bool = False):
        """
        Execute query and return result.
        """
        result = await session.execute(query)

        if result:
            if many:
                return result.scalars().all()
            return result.scalars().first()

    @staticmethod
    async def _make_filter(model, filters: dict, contains: bool) -> select:
        """
        First generate a list of filters based on given parameters.
        Then apply filters to query.
        """
        # If contains is True, then use LIKE operator
        if contains:
            filter_conditions = [
                cast(getattr(model, field), String).like(f"%{value}%")
                for field, value in filters.items()
            ]
            return select(model).where(or_(*filter_conditions))

        # Otherwise use equality operator
        filter_conditions = [
            getattr(model, field) == value for field, value in filters.items()
        ]
        return select(model).where(and_(*filter_conditions))

    @staticmethod
    async def _make_joins(model, query, join_fields: Optional[List[str]] = None):
        """
        Make joins for query based on given list of fields.
        """
        if join_fields is not None:
            for field in join_fields:
                query = query.options(selectinload(getattr(model, field)))
        return query

    @staticmethod
    async def _create_order_by(
        model, query, order_by: Optional[list] = None, descending: bool = False
    ):
        """
        Create order by for query based on given list of fields.
        """
        if order_by is not None:
            for field in order_by:
                if descending:
                    query = query.order_by(desc(getattr(model, field)))
                else:
                    query = query.order_by(asc(getattr(model, field)))
        return query
