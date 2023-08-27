import pytest_asyncio
from src.app.models import Product
from src.app.controllers import ProductController
from src.app.repositories import ProductRepository


@pytest_asyncio.fixture
async def product_controller(get_test_db, get_test_redis):
    """
    Return a product controller
    """
    return ProductController(
        repository=ProductRepository(
            model=Product, database=get_test_db, redis=get_test_redis
        )
    )


@pytest_asyncio.fixture
async def product(product_controller, accepted_vendor, user):
    """
    Create and return a product
    """
    product = await product_controller.create(
        request_user=user,
        request_vendor=accepted_vendor,
        data={
            "title": "Test Product",
            "description": "Test Product Description",
            "price": 100,
            "specs": {"test": "test"},
        },
    )

    return product
