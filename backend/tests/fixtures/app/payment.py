import pytest_asyncio
from src.app.models import Payment
from src.app.controllers import PaymentController
from src.app.repositories import PaymentRepository


@pytest_asyncio.fixture
async def payment_controller(get_test_db, get_test_redis):
    """
    Payment controller fixture
    """
    return PaymentController(
        repository=PaymentRepository(
            model=Payment, database_session=get_test_db, redis_session=get_test_redis
        )
    )
