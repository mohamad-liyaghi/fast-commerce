import pytest_asyncio
from src.app.models import Payment
from src.app.controllers import PaymentController
from src.app.repositories import PaymentRepository
from src.app.enums import OrderStatusEnum


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


@pytest_asyncio.fixture
async def payment(payment_controller, order, admin, order_controller):
    """
    Payment fixture
    """
    await order_controller._set_paid(order=order)
    return await payment_controller.create(
        user=admin,
        order=order,
        amount=order.total_price,
    )
