import pytest


class TestUserModel:
    @pytest.mark.asyncio
    async def test_user_is_not_vendor(self, user, vendor_controller):
        assert not await vendor_controller.retrieve_accepted_vendor(user=user)

    @pytest.mark.asyncio
    async def test_user_is_vendor(self, accepted_vendor, vendor_controller):
        user = accepted_vendor.owner
        assert await vendor_controller.retrieve_accepted_vendor(user=user)

    @pytest.mark.asyncio
    async def test_user_not_vendor_rejected(self, rejected_vendor, vendor_controller):
        """
        Users with only rejected vendors should not be vendors
        """
        user = rejected_vendor.owner
        assert not await vendor_controller.retrieve_accepted_vendor(user=user)

    @pytest.mark.asyncio
    async def test_user_not_vendor_pending(self, pending_vendor, vendor_controller):
        """
        Users with only pending vendors should not be vendors
        """
        user = pending_vendor.owner
        assert not await vendor_controller.retrieve_accepted_vendor(user=user)
