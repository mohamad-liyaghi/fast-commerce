from redis import Redis
from .create import BaseCacheCreateRepository
from .delete import BaseCacheDeleteRepository
from .retrieve import BaseCacheRetrieveRepository


class BaseCacheRepository(
    BaseCacheCreateRepository, BaseCacheRetrieveRepository, BaseCacheDeleteRepository
):
    """
    This repository is responsible for all the cache operations
    """

    def __init__(self, redis_client: Redis):
        self.client = redis_client
