import pytest_asyncio
from src.app.models import OrderItem
from src.app.controllers import OrderItemController
from src.app.repositories import OrderItemRepository


@pytest_asyncio.fixture
async def order_item_controller(get_test_db, get_test_redis):
    """
    Return an order item controller
    """
    return OrderItemController(
        repository=OrderItemRepository(
            model=OrderItem, database_session=get_test_db, redis_session=get_test_redis
        )
    )
