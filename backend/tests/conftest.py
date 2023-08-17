import pytest_asyncio, pytest, asyncio
from tests.fixtures.db import get_test_db # noqa
from tests.fixtures.client import * # noqa
from tests.fixtures.user import * # noqa
from tests.fixtures.redis import * # noqa


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def flush_redis(get_test_redis):
    """
    Flush redis before each test
    """
    await get_test_redis.flushall()
