from sqlalchemy.orm import Session
from core.database import Base


class BaseRepository:
    """
    Base repository class
    Methods:
        create: Create a new instance of model
        update: Update an instance of model
        delete: Delete an instance of model
        retrieve: Retrieve an instance of model
        list: List all instances of model
    """
    def __init__(self, model: Base, database: Session):
        self.model = model
        self.database = database

    def create(self, **data):
        """
        Create a new instance of model
        :param data: data to create new instance
        :return: created instance
        """
        instance = self.model(**data)
        self.database.add(instance)
        self.database.commit()
        self.database.refresh(instance)
        return instance

    def update(self, instance: Base, **data):
        """
        Update an instance of model
        :param instance: instance to update
        :param data: data to update
        :return: updated instance
        """
        for key, value in data.items():
            setattr(instance, key, value)
        self.database.commit()
        self.database.refresh(instance)
        return instance

    def delete(self, instance: Base):
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        self.database.delete(instance)
        self.database.commit()

    def retrieve(self, many: bool = False, **kwargs):
        """
        Retrieve an instance of model
        :param kwargs: filter parameters
        :param many: retrieve many instances
        :return: instance
        """
        query = self.database.query(self.model).filter_by(**kwargs)
        return query.all() if many else query.first()

    def list(self, limit: int = 100, skip: int = 0, **kwargs):
        """
        List all instances of model
        :param limit: limit of instances
        :param skip: skip instances
        :param kwargs: filter parameters
        :return: list of instances
        """
        query = (self.database.query(self.model).
                 filter_by(**kwargs).
                 offset(skip).
                 limit(limit))

        return query.all()
