from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from typing import Optional, List
from uuid import UUID
from src.app.repositories.base import BaseRepository
from .cache import BaseCacheController


class BaseController(BaseCacheController):
    """
    Base controller class
    Methods:
        create: Create a new instance of model
        update: Update an instance of model
        delete: Delete an instance of model
        retrieve: Retrieve an instance of model
        list: List all instances of model
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def get_by_id(self, _id: int, join_fields: Optional[List[str]] = None):
        """
        Get an instance by id
        :param _id: id of instance
        :param join_fields: fields to join
        :return: instance
        """
        result = await self.retrieve(id=_id, join_fields=join_fields)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="item not found."
            )
        return result

    async def get_by_uuid(self, uuid: UUID, join_fields: Optional[List[str]] = None):
        """
        Get an instance by uuid
        :param uuid: uuid of instance
        :param join_fields: fields to join
        :return: instance
        """
        result = await self.retrieve(uuid=uuid, join_fields=join_fields)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="item not found."
            )
        return result

    async def create(self, **data):
        """
        Create a new instance of model
        :param data: data to create new instance
        :return: created instance
        """
        result = await self.repository.create(**data)
        return result

    async def update(self, instance, **data):
        """
        Update an instance of model
        :param instance: instance to update
        :param data: data to update
        :return: updated instance
        """
        result = await self.repository.update(instance, **data)
        return result

    async def delete(self, instance):
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        await self.repository.delete(instance)
        return

    async def retrieve(
        self,
        join_fields: Optional[selectinload] = None,
        many: bool = False,
        last: bool = False,
        **kwargs
    ):
        """
        Retrieve an instance of model
        :param kwargs: filter parameters
        :param join_fields: fields to join
        :param many: retrieve many instances
        :param last: retrieve last instance
        :return: instance
        """
        result = await self.repository.retrieve(
            join_fields, many=many, last=last, **kwargs
        )
        return result if result else None

    async def list(self, limit: int = 100, skip: int = 0, **kwargs):
        """
        List all instances of model
        :param kwargs: filter parameters
        :param limit: limit of instances
        :param skip: skip instances
        :return: instances
        """
        result = await self.repository.list(limit=limit, skip=skip, **kwargs)
        return result if result else None
