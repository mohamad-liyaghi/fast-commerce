import pytest_asyncio
from src.app.controllers import CartController
from src.app.repositories import CartRepository


@pytest_asyncio.fixture
async def cart_controller(get_test_redis):
    """
    Return a cart controller
    """
    return CartController(repository=CartRepository(redis_client=get_test_redis))


@pytest_asyncio.fixture
async def cart(product, admin, cart_controller, product_controller):
    """
    Create and return a cart
    """
    cart_data = {
        "product_uuid": str(product.uuid),
        "quantity": 1,
    }
    await cart_controller.add_item(
        product_controller=product_controller, request_user=admin, **cart_data
    )
    return cart_data
