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
