import pytest_asyncio
from src.app.controllers import CartController
from src.app.repositories import CartRepository
from src.core.utils import format_key
from src.core.configs import settings


@pytest_asyncio.fixture(scope="session")
async def cart_controller(get_test_redis):
    """
    Return a cart controller
    """
    return CartController(repository=CartRepository(redis_client=get_test_redis))


@pytest_asyncio.fixture(scope="session")
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
    key = await format_key(key=settings.CACHE_CART_KEY, user_uuid=admin.uuid)
    cart = await cart_controller.get_cache(key=key)
    return cart
