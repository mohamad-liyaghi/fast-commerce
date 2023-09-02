from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from src.core.database import Base
from .cache import BaseCacheRepository
from .database import BaseDatabaseRepository


class BaseRepository(BaseDatabaseRepository, BaseCacheRepository):
    """
    Base repository class which handels both database and cache operations
    """

    def __init__(
        self, model: Base, database_session: AsyncSession, redis_session: Redis
    ):
        BaseDatabaseRepository.__init__(self, model=model, db_session=database_session)
        BaseCacheRepository.__init__(self, redis_client=redis_session)

