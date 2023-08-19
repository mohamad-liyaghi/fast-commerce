import pytest_asyncio
from tests.shared.db import get_test_db as get_test_db_func


@pytest_asyncio.fixture
async def get_test_db():
    yield next(get_test_db_func())
