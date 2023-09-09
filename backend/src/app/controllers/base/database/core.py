from src.app.repositories.base import BaseRepository
from .create import BaseCreateController
from .update import BaseUpdateController
from .delete import BaseDeleteController
from .retrieve import BaseRetrieveController


class BaseDatabaseController(
    BaseCreateController,
    BaseUpdateController,
    BaseDeleteController,
    BaseRetrieveController,
):
    """
    Base controller class
    This class inherits from all the other base controllers
    which are used to handle CRUD operations.
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository
