from fastapi import HTTPException, status
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

    async def get_by_id(self, _id: int):
        """
        Get an instance by id
        :param _id: id of instance
        :return: instance
        """
        result = await self.retrieve(id=_id)
        return result if result else None

    async def get_by_uuid(self, uuid: UUID):
        """
        Get an instance by uuid
        :param uuid: uuid of instance
        :return: instance
        """
        result = await self.retrieve(uuid=uuid)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
            )
        return result

    async def create(self, **data):
        """
        Create a new instance of model
        :param data: data to create new instance
        :return: created instance
        """
        result = await self.repository.create(**data)
        return result if result else None

    async def update(self, instance, **data):
        """
        Update an instance of model
        :param instance: instance to update
        :param data: data to update
        :return: updated instance
        """
        result = await self.repository.update(instance, **data)
        return result if result else None

    async def delete(self, instance):
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        result = await self.repository.delete(instance)
        return result if result else None

    async def retrieve(self, many: bool = False, last: bool = False, **kwargs):
        """
        Retrieve an instance of model
        :param kwargs: filter parameters
        :param many: retrieve many instances
        :param last: retrieve last instance
        :return: instance
        """
        result = await self.repository.retrieve(many, last, **kwargs)
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
