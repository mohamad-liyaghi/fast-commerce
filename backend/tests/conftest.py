import pytest
import pytest_asyncio  # noqa
import asyncio
from tests.fixtures.db import get_test_db  # noqa
from tests.fixtures.client import *  # noqa
from tests.fixtures.app import *  # noqa
from tests.fixtures.redis import *  # noqa
from src.core.celery import celery


@pytest.fixture(scope="class")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="class")
async def flush_redis(get_test_redis):
    """
    Flush redis before each test
    """
    await get_test_redis.flushall()


@pytest_asyncio.fixture(autouse=True, scope="class")
async def set_celery_eager():
    celery.conf.task_always_eager = True
    yield
    celery.conf.task_always_eager = False
