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
        }  # TODO: Update this information with faker
        self.controller = vendor_controller

    @pytest.mark.asyncio
    async def test_create(self, user):
        await self.controller.create(request_user=user, **self.data)
        assert await self.controller.list() is not None

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
            rejected_vendor, reviewed_at=reviewed_at
        )
        assert await self.controller.list() is not None
