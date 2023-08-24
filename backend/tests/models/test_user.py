import pytest


class TestUserModel:
    @pytest.mark.asyncio
    async def test_user_is_vendor(self, accepted_vendor):
        user = accepted_vendor.owner
        assert not await user.get_accepted_vendor()

    @pytest.mark.asyncio
    async def test_user_is_not_vendor(self, user):
        assert not await user.get_accepted_vendor()

    @pytest.mark.asyncio
    async def test_user_not_vendor_rejected(self, rejected_vendor):
        """
        Users with only rejected vendors should not be vendors
        """
        user = rejected_vendor.owner
        assert not await user.get_accepted_vendor()

    @pytest.mark.asyncio
    async def test_user_not_vendor_pending(self, pending_vendor):
        """
        Users with only pending vendors should not be vendors
        """
        user = pending_vendor.owner
        assert not await user.get_accepted_vendor()
