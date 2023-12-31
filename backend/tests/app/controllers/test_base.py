import pytest
from tests.utils.faker import create_fake_credential


class TestBaseController:
    @pytest.fixture(autouse=True)
    def setup(self, user_controller):
        # NOTE: We can use any controller cuz
        # they all inherit from BaseController
        self.controller = user_controller

    @pytest.mark.asyncio
    async def test_create_valid_data(self):
        credentials = await create_fake_credential()
        user = await self.controller.create(**credentials)
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_create_and_hash_password(self):
        credential = await create_fake_credential()
        password = credential.get("password")
        user = await self.controller.create(**credential)
        assert user.password != password

    @pytest.mark.asyncio
    async def test_retrieve_existing_record(self, user):
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
    async def test_update_existing_record(self, user):
        new_first_name = "new name"
        result = await self.controller.repository.update(
            user, first_name=new_first_name
        )
        assert result.first_name == new_first_name

    @pytest.mark.asyncio
    async def test_non_empty_list(self, user):
        result = await self.controller.retrieve(many=True)
        assert result is not None
        assert user in result

    @pytest.mark.asyncio
    async def test_update_and_hash_password(self, user):
        """
        When user updates its password, the new pass gets hashed
        """
        password = "1234"
        result = await self.controller.repository.update(user, password=password)
        assert not result.password == password

    @pytest.mark.asyncio
    async def test_retrieve_record_with_contains_param(self, user):
        email = user.email[:5]
        result = await self.controller.retrieve(email=email, contains=True)
        assert result

    @pytest.mark.asyncio
    async def test_retrieve_without_contain_param(self, user):
        email = user.email[:5]
        result = await self.controller.retrieve(email=email)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_existing_record(self, user):
        result = await self.controller.delete(user)
        assert result is None
