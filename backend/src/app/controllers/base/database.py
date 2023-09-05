from fastapi import HTTPException, status
from typing import Optional, List
from uuid import UUID
from src.app.repositories.base import BaseRepository


class BaseDatabaseController:
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

    async def get_by_id(
        self,
        _id: int,
        join_fields: Optional[List[str]] = None,
        not_found_message: str = "item not found",
    ):
        """
        Get an instance by id
        :param _id: id of instance
        :param join_fields: fields to join
        :param not_found_message: message to raise if instance not found
        :return: instance
        """
        result = await self.retrieve(id=_id, join_fields=join_fields)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=not_found_message
            )
        return result

    async def get_by_uuid(
        self,
        uuid: UUID | str,
        join_fields: Optional[List[str]] = None,
        not_found_message: str = "item not found",
    ):
        """
        Get an instance by uuid
        :param uuid: UUID | str of instance
        :param join_fields: fields to join
        :param not_found_message: message to raise if instance not found
        :return: instance
        """
        result = await self.retrieve(uuid=uuid, join_fields=join_fields)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=not_found_message
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

    async def delete(self, instance, **kwargs):
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        await self.repository.delete(instance, **kwargs)
        return

    async def retrieve(
        self,
        join_fields: Optional[List[str]] = None,
        order_by: Optional[list] = None,
        many: bool = False,
        descending: bool = False,
        limit: int = 100,
        skip: int = 0,
        contains: bool = False,
        **kwargs
    ):
        """
        Retrieve an instance of model
        :param join_fields: fields to join
        :param order_by: order by fields
        :param many: retrieve many instances
        :param descending: descending order
        :param limit: limit of instances
        :param skip: offset of instances
        :param kwargs: filter parameters
        :return: instance
        """
        result = await self.repository.retrieve(
            join_fields=join_fields,
            limit=limit,
            skip=skip,
            many=many,
            descending=descending,
            order_by=order_by,
            contains=contains,
            **kwargs
        )
        return result if result else None
