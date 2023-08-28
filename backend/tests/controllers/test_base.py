import pytest
from tests.utils.mocking import create_fake_credential


class TestBaseController:
    @pytest.fixture(autouse=True)
    def setup(self, user_controller):
        # NOTE: We can use any controller cuz
        # they all inherit from BaseController
        self.controller = user_controller

    @pytest.mark.asyncio
    async def test_create(self):
        credentials = await create_fake_credential()
        user = await self.controller.create(**credentials)
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_retrieve(self, user):
        result = await self.controller.retrieve(id=user.id)
        assert result.id == user.id

    @pytest.mark.asyncio
    async def test_get_by_id(self, user):
        result = await self.controller.get_by_id(user.id)
        assert result.id == user.id

    @pytest.mark.asyncio
    async def test_get_by_uuid(self, user):
        result = await self.controller.get_by_uuid(user.uuid)
        assert result.uuid == user.uuid

    @pytest.mark.asyncio
    async def test_update(self, user):
        new_first_name = "new name"
        result = await self.controller.repository.update(
            user, first_name=new_first_name
        )
        assert result.first_name == new_first_name

    @pytest.mark.asyncio
    async def test_delete(self, user):
        result = await self.controller.delete(user)
        assert result is None

    @pytest.mark.asyncio
    async def test_list(self, user):
        result = await self.controller.list()
        assert result is not None

    @pytest.mark.asyncio
    async def test_empty_list(self):
        result = await self.controller.list()
        assert result is None

    @pytest.mark.asyncio
    async def test_list_password_is_hashed(self):
        credential = await create_fake_credential()
        password = credential.get("password")

        user = await self.controller.create(**credential)
        assert user.password != password

    @pytest.mark.asyncio
    async def test_update_password(self, user):
        """
        When user updates its password, the new pass gets hashed
        """
        password = "1234"
        result = await self.controller.repository.update(user, password=password)

        assert not result.password == password
