import pytest_asyncio
from tests.shared.redis import override_get_redis


@pytest_asyncio.fixture
async def get_test_redis():
    redis = await override_get_redis()
    yield redis
