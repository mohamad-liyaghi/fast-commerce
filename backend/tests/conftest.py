import pytest
import asyncio
from tests.fixtures.db import get_test_db  # noqa
from tests.fixtures.client import *  # noqa
from tests.fixtures.app import *  # noqa
from tests.fixtures.redis import *  # noqa
from src.core.celery import celery


@pytest.fixture(scope="session")
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


@pytest_asyncio.fixture(autouse=True)
async def set_celery_eager():
    celery.conf.task_always_eager = True
    yield
    celery.conf.task_always_eager = False
