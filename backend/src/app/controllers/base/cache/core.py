from src.app.repositories.base import BaseRepository
from .create import BaseCacheCreateController
from .delete import BaseCacheDeleteController
from .retrieve import BaseCacheRetrieveController


class BaseCacheController(
    BaseCacheCreateController, BaseCacheRetrieveController, BaseCacheDeleteController
):
    """
    This class is a composition of all cache controllers.
    It is used to create a new record, update, retrieve and delete a record in cache.
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository
