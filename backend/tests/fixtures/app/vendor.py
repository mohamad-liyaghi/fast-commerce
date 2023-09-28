import pytest_asyncio
from datetime import datetime, timedelta
from src.app.models import Vendor
from src.app.enums import VendorStatusEnum
from src.app.controllers import VendorController
from src.app.repositories import VendorRepository


@pytest_asyncio.fixture(scope="class")
async def vendor_controller(get_test_db, get_test_redis):
    """
    Returns a UserController instance
    """
    return VendorController(
        repository=VendorRepository(
            model=Vendor, database_session=get_test_db, redis_session=get_test_redis
        )
    )


@pytest_asyncio.fixture(scope="class")
async def pending_vendor(vendor_controller, user, admin):
    """
    Returns a pending vendor
    """
    vendor = await vendor_controller.create(
        request_user=user,
        name="Test Vendor",
        description="Test Description",
        domain="test.com",
        address="Test Address",
        reviewer_id=admin.id,
    )
    return vendor


@pytest_asyncio.fixture(scope="class")
async def accepted_vendor(vendor_controller, admin, pending_vendor):
    """
    Returns accepted vendor
    """
    vendor = await vendor_controller.update(
        request_user=admin,
        instance=pending_vendor,
        status=VendorStatusEnum.ACCEPTED,
    )
    return vendor


@pytest_asyncio.fixture(scope="class")
async def rejected_vendor(vendor_controller, admin, pending_vendor):
    """
    Returns a rejected vendor
    """
    vendor = await vendor_controller.update(
        request_user=admin,
        instance=pending_vendor,
        status=VendorStatusEnum.REJECTED,
        reviewed_at=datetime.utcnow(),
    )
    return vendor


@pytest_asyncio.fixture(scope="class")
async def old_rejected_vendor(vendor_controller, admin, pending_vendor):
    reviewed_at = datetime.utcnow() - timedelta(days=11)
    vendor = await vendor_controller.update(
        request_user=admin,
        instance=pending_vendor,
        status=VendorStatusEnum.REJECTED,
        reviewed_at=reviewed_at,
    )
    return vendor
