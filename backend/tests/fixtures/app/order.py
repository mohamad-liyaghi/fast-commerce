import pytest_asyncio
from src.app.models import Order
from src.app.controllers import OrderController
from src.app.repositories import OrderRepository


@pytest_asyncio.fixture
async def order_controller(get_test_db, get_test_redis):
    """
    Return an order controller
    """
    return OrderController(
        repository=OrderRepository(
            model=Order, database_session=get_test_db, redis_session=get_test_redis
        )
    )
