import pytest
from tests.utils import create_fake_credential


class TestUserController:

    @pytest.mark.asyncio
    async def test_create(self, user_controller):
        user = await user_controller.create(**create_fake_credential())
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_retrieve(self, user_controller, user):
        result = await user_controller.retrieve(id=user.id)
        assert result.id == user.id

    @pytest.mark.asyncio
    async def test_get_by_id(self, user_controller, user):
        result = await user_controller.get_by_id(user.id)
        assert result.id == user.id

    @pytest.mark.asyncio
    async def test_get_by_uuid(self, user_controller, user):
        result = await user_controller.get_by_uuid(user.uuid)
        assert result.uuid == user.uuid

    @pytest.mark.asyncio
    async def test_update(self, user_controller, user):
        new_first_name = 'new name'
        result = await user_controller.update(user, first_name=new_first_name)
        assert result.first_name == new_first_name

    @pytest.mark.asyncio
    async def test_delete(self, user_controller, user):
        result = await user_controller.delete(user)
        assert result is None

    @pytest.mark.asyncio
    async def test_list(self, user_controller):
        result = await user_controller.list()
        assert result is not None
