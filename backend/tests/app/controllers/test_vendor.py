from fastapi import HTTPException
import pytest
import asyncio
from src.app.enums import VendorStatusEnum
from tests.utils.faker import create_vendor_credential


class TestVendorController:
    @pytest.fixture(autouse=True)
    def setup(self, vendor_controller):
        self.data = asyncio.run(create_vendor_credential())
        self.controller = vendor_controller

    @pytest.mark.asyncio
    async def test_create_pending_exists(self, user, pending_vendor):
        assert pending_vendor.status == VendorStatusEnum.PENDING
        with pytest.raises(HTTPException):
            await self.controller.create(request_user=user, **self.data)

    @pytest.mark.asyncio
    async def test_create_accepted_exists(self, user, accepted_vendor):
        assert accepted_vendor.status == VendorStatusEnum.ACCEPTED
        with pytest.raises(HTTPException):
            await self.controller.create(request_user=user, **self.data)

    @pytest.mark.asyncio
    async def test_create_rejected_exists(self, user, rejected_vendor):
        assert rejected_vendor.status == VendorStatusEnum.REJECTED
        with pytest.raises(HTTPException):
            await self.controller.create(request_user=user, **self.data)

    @pytest.mark.asyncio
    async def test_create_old_rejected_exist(self, old_rejected_vendor):
        assert await self.controller.retrieve(many=True) is not None
        assert old_rejected_vendor.status == VendorStatusEnum.REJECTED

    @pytest.mark.asyncio
    async def test_update_by_owner(self, accepted_vendor):
        domain = "https://www.update_vendord.com"
        updated_vendor = await self.controller.update_vendor(
            request_user=accepted_vendor.owner,
            domain=domain,
            vendor_uuid=accepted_vendor.uuid,
        )
        assert updated_vendor.domain == domain

    @pytest.mark.asyncio
    async def test_update_by_admin(self, admin, accepted_vendor):
        """
        Admins cannot update vendors credentials.
        """
        with pytest.raises(HTTPException):
            await self.controller.update_vendor(
                request_user=admin,
                vendor_uuid=accepted_vendor.uuid,
                domain="https://www.updated.com",
            )

    @pytest.mark.asyncio
    async def test_update_status_by_admin(self, admin, accepted_vendor):
        """
        Admins can update vendors status.
        """
        updated_vendor = await self.controller.update_vendor(
            request_user=admin,
            vendor_uuid=accepted_vendor.uuid,
            status=VendorStatusEnum.REJECTED,
        )
        assert updated_vendor.status == VendorStatusEnum.REJECTED

    @pytest.mark.asyncio
    async def test_update_status_by_owner(self, accepted_vendor):
        """Owners are not allowed to update vendor status."""
        with pytest.raises(HTTPException):
            await self.controller.update_vendor(
                request_user=accepted_vendor.owner,
                vendor_uuid=accepted_vendor.uuid,
                status=VendorStatusEnum.REJECTED,
            )

    @pytest.mark.asyncio
    async def test_create(self, user, accepted_vendor):
        await self.controller.repository.delete(instance=accepted_vendor)
        await self.controller.create(request_user=user, **self.data)
        assert await self.controller.retrieve(many=True) is not None
