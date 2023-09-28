import pytest
from tests.utils.faker import create_vendor_credential
from src.app.repositories import VendorRepository
from src.app.models import Vendor
from src.app.enums import VendorStatusEnum
from src.core.exceptions import (
    PendingVendorExistsException,
    AcceptedVendorExistsException,
    RejectedVendorExistsException,
    UpdateVendorStatusDenied,
    VendorInformationUpdateDenied,
)


class TestVendorRepository:
    @pytest.fixture(autouse=True)
    def setup(self, get_test_db, get_test_redis):
        self.redis = get_test_redis
        self.repository = VendorRepository(
            model=Vendor, database_session=get_test_db, redis_session=get_test_redis
        )

    @pytest.mark.asyncio
    async def test_create_vendor_pending_exists(self, user, pending_vendor):
        credential = await create_vendor_credential()
        assert pending_vendor.status == VendorStatusEnum.PENDING
        with pytest.raises(PendingVendorExistsException):
            await self.repository.create(request_user=user, **credential)

    @pytest.mark.asyncio
    async def test_create_vendor_accepted_exists(self, user, accepted_vendor):
        credential = await create_vendor_credential()
        assert accepted_vendor.status == VendorStatusEnum.ACCEPTED
        with pytest.raises(AcceptedVendorExistsException):
            await self.repository.create(request_user=user, **credential)

    @pytest.mark.asyncio
    async def test_create_vendor_rejected_exists(self, user, rejected_vendor):
        credential = await create_vendor_credential()
        assert rejected_vendor.status == VendorStatusEnum.REJECTED
        with pytest.raises(RejectedVendorExistsException):
            await self.repository.create(request_user=user, **credential)

    @pytest.mark.asyncio
    async def test_create_old_rejected_exists(self, user, old_rejected_vendor):
        credential = await create_vendor_credential()
        vendor = await self.repository.create(request_user=user, **credential)

        assert old_rejected_vendor.status == VendorStatusEnum.REJECTED
        assert vendor.owner_id == user.id

    @pytest.mark.asyncio
    async def test_update_vendor(self, user, accepted_vendor):
        credential = await create_vendor_credential()
        vendor = await self.repository.update_vendor(
            request_user=user, instance=accepted_vendor, **credential
        )
        assert vendor.owner_id == user.id

    @pytest.mark.asyncio
    async def test_update_vendor_status_by_admin(self, admin, accepted_vendor):
        vendor = await self.repository.update_vendor(
            request_user=admin,
            instance=accepted_vendor,
            status=VendorStatusEnum.REJECTED,
        )
        assert vendor.status == VendorStatusEnum.REJECTED

    @pytest.mark.asyncio
    async def test_update_vendor_status_denied(self, user, accepted_vendor):
        with pytest.raises(UpdateVendorStatusDenied):
            await self.repository.update_vendor(
                request_user=user,
                instance=accepted_vendor,
                status=VendorStatusEnum.REJECTED,
            )

    @pytest.mark.asyncio
    async def test_update_vendor_denied_by_admin(self, admin, accepted_vendor):
        credential = await create_vendor_credential()
        with pytest.raises(VendorInformationUpdateDenied):
            await self.repository.update_vendor(
                request_user=admin, instance=accepted_vendor, **credential
            )
