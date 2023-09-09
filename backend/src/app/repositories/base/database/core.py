from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import Base
from .create import BaseCreateRepository
from .delete import BaseDeleteRepository
from .retrieve import BaseRetrieveRepository
from .update import BaseUpdateRepository


class BaseDatabaseRepository(
    BaseCreateRepository,
    BaseRetrieveRepository,
    BaseUpdateRepository,
    BaseDeleteRepository,
):
    """
    This class is a composition of all database repositories.
    It is used to create a new record, update, retrieve and delete a record in database.
    """

    def __init__(self, model: Base, db_session: AsyncSession):
        self.model = model
        self.session = db_session  # Database session
