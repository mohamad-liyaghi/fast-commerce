import pytest_asyncio
from src.app.models import Product
from src.app.controllers import ProductController
from src.app.repositories import ProductRepository
from tests.utils.faker import create_product_credential


@pytest_asyncio.fixture(scope="session")
async def product_controller(get_test_db, get_test_redis):
    """
    Return a product controller
    """
    return ProductController(
        repository=ProductRepository(
            model=Product, database_session=get_test_db, redis_session=get_test_redis
        )
    )


@pytest_asyncio.fixture(scope="session")
async def product(product_controller, accepted_vendor, user):
    """
    Create and return a product
    """
    credentials = await create_product_credential()
    product = await product_controller.create(
        request_user=user,
        request_vendor=accepted_vendor,
        data={**credentials},
    )

    return product
