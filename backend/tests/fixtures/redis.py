import pytest_asyncio
from tests.mocks import override_get_redis


@pytest_asyncio.fixture(scope="class")
async def get_test_redis():
    redis = await override_get_redis()
    yield redis
