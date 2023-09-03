from fastapi import HTTPException
import pytest
from datetime import datetime, timedelta
from src.app.models import VendorStatus


class TestVendorController:
    @pytest.fixture(autouse=True)
    def setup(self, vendor_controller):
        self.data = {
            "name": "Test Vendor",
            "description": "Test Description",
            "domain": "test.com",
            "address": "Test Address",
        }
        self.controller = vendor_controller

    @pytest.mark.asyncio
    async def test_create(self, user):
        await self.controller.create(request_user=user, **self.data)
        assert await self.controller.retrieve(many=True) is not None

    @pytest.mark.asyncio
    async def test_create_pending_exists(self, user, pending_vendor):
        assert pending_vendor.status == VendorStatus.PENDING
        with pytest.raises(HTTPException):
            await self.controller.create(request_user=user, **self.data)

    @pytest.mark.asyncio
    async def test_create_accepted_exists(self, user, accepted_vendor):
        assert accepted_vendor.status == VendorStatus.ACCEPTED
        with pytest.raises(HTTPException):
            await self.controller.create(request_user=user, **self.data)

    @pytest.mark.asyncio
    async def test_create_rejected_exists(self, user, rejected_vendor):
        assert rejected_vendor.status == VendorStatus.REJECTED
        with pytest.raises(HTTPException):
            await self.controller.create(request_user=user, **self.data)

    @pytest.mark.asyncio
    async def test_create_old_rejected_exist(self, rejected_vendor):
        assert rejected_vendor.status == VendorStatus.REJECTED
        reviewed_at = datetime.utcnow() - timedelta(days=11)
        await self.controller.repository.update(
            instance=rejected_vendor,
            reviewed_at=reviewed_at,
            request_user=rejected_vendor.owner,
        )
        assert await self.controller.retrieve(many=True) is not None

    @pytest.mark.asyncio
    async def test_update_by_owner(self, accepted_vendor):
        domain = "https://www.updated.com"
        updated_vendor = await self.controller.update(
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
            await self.controller.update(
                request_user=admin,
                vendor_uuid=accepted_vendor.uuid,
                domain="https://www.updated.com",
            )

    @pytest.mark.asyncio
    async def test_update_status_by_admin(self, admin, accepted_vendor):
        """
        Admins can update vendors status.
        """
        updated_vendor = await self.controller.update(
            request_user=admin,
            vendor_uuid=accepted_vendor.uuid,
            status=VendorStatus.REJECTED,
        )
        assert updated_vendor.status == VendorStatus.REJECTED

    @pytest.mark.asyncio
    async def test_update_status_by_owner(self, accepted_vendor):
        """Owners are not allowed to update vendor status."""
        with pytest.raises(HTTPException):
            await self.controller.update(
                request_user=accepted_vendor.owner,
                vendor_uuid=accepted_vendor.uuid,
                status=VendorStatus.REJECTED,
            )
