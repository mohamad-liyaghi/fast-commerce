import pytest
from uuid import uuid4
from fastapi import HTTPException


class TestUserController:
    @pytest.mark.asyncio
    async def test_get_by_uuid(self, user_controller, user):
        result = await user_controller.get_by_uuid(uuid=user.uuid)
        assert result.uuid == user.uuid

    @pytest.mark.asyncio
    async def test_get_by_uuid_not_found(self, user_controller):
        """
        Raise HTTPException when user not found
        """
        with pytest.raises(HTTPException):
            await user_controller.get_by_uuid(uuid=uuid4())

    @pytest.mark.asyncio
    async def test_update(self, user_controller, user):
        """
        Only profile owner can update its profile
        """
        updated_first_name = "updated first name"
        updated_user = await user_controller.update(
            uuid=user.uuid, requesting_user=user, first_name=updated_first_name
        )
        assert updated_user.first_name == updated_first_name
        assert updated_user == user

    @pytest.mark.asyncio
    async def test_update_by_others(self, user_controller, user, admin):
        """
        No one can update others data
        """
        with pytest.raises(HTTPException):
            await user_controller.update(
                uuid=user.uuid, requesting_user=admin, first_name="updated one"
            )
