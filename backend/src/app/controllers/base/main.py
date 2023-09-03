from src.app.repositories.base import BaseRepository
from .cache import BaseCacheController
from .database import BaseDatabaseController


class BaseController(BaseDatabaseController, BaseCacheController):
    """
    Base controller class which handles both database and cache operations
    """

    def __init__(self, repository: BaseRepository):
        BaseDatabaseController.__init__(self, repository=repository)
        BaseCacheController.__init__(self, repository=repository)
