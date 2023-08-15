from uuid import UUID
from core.repository import BaseRepository


class BaseController:
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

    def get_by_id(self, _id: int):
        """
        Get an instance by id
        :param _id: id of instance
        :return: instance
        """
        return self.retrieve(id=_id)

    def get_by_uuid(self, uuid: UUID):
        """
        Get an instance by uuid
        :param uuid: uuid of instance
        :return: instance
        """
        return self.retrieve(uuid=uuid)

    def create(self, **data):
        """
        Create a new instance of model
        :param data: data to create new instance
        :return: created instance
        """
        return self.repository.create(**data)

    def update(self, instance, **data):
        """
        Update an instance of model
        :param instance: instance to update
        :param data: data to update
        :return: updated instance
        """
        return self.repository.update(instance, **data)

    def delete(self, instance):
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        return self.repository.delete(instance)

    def retrieve(self, many: bool = False, **kwargs):
        """
        Retrieve an instance of model
        :param kwargs: filter parameters
        :param many: retrieve many instances
        :return: instance
        """
        return self.repository.retrieve(many, **kwargs)

    def list(self, limit: int = 100, skip: int = 0, **kwargs):
        """
        List all instances of model
        :param kwargs: filter parameters
        :param limit: limit of instances
        :param skip: skip instances
        :return: instances
        """
        return self.repository.list(limit=limit, skip=skip, **kwargs)
