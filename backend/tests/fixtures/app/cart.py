import pytest_asyncio
from src.app.controllers import CartController
from src.app.repositories import CartRepository


@pytest_asyncio.fixture
async def cart_controller(get_test_redis):
    """
    Return a cart controller
    """
    return CartController(repository=CartRepository(redis_clint=get_test_redis))
