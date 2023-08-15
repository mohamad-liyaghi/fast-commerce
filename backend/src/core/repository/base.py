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

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def retrieve(self):
        pass

    def list(self):
        pass