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


@pytest_asyncio.fixture
async def preparing_order_item(
    accepted_vendor, paid_order, order_item_controller, product
):
    order_item = await order_item_controller.create(
        order_id=paid_order.id,
        product_id=product.id,
        quantity=1,
        total_price=product.price,
        vendor_id=accepted_vendor.id,
    )
    return order_item
