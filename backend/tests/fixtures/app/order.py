import pytest_asyncio
from src.app.models import Order
from src.app.controllers import OrderController
from src.app.repositories import OrderRepository
from src.app.enums import OrderStatusEnum


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


@pytest_asyncio.fixture
async def order(
    admin,
    cart,
    order_controller,
    order_item_controller,
    cart_controller,
    product_controller,
):
    order = await order_controller.create_order(
        request_user=admin,
        order_item_controller=order_item_controller,
        cart_controller=cart_controller,
        cart=cart,
        product_controller=product_controller,
        delivery_address="test address",
    )
    return order


@pytest_asyncio.fixture
async def paid_order(
    admin,
    cart,
    order_controller,
    order_item_controller,
    cart_controller,
    product_controller,
):
    order = await order_controller.create_order(
        request_user=admin,
        order_item_controller=order_item_controller,
        cart_controller=cart_controller,
        cart=cart,
        product_controller=product_controller,
        delivery_address="test address",
        status=OrderStatusEnum.PREPARING,
    )
    return order
