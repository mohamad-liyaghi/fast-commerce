import pytest
from tests.utils.mocking import create_fake_credential
from src.app.repositories import BaseRepository
from src.app.models import User


class TestBaseRepository:
    @pytest.fixture(autouse=True)
    def setup(self, get_test_db, get_test_redis):
        self.repository = BaseRepository(
            model=User, database=get_test_db, redis=get_test_redis
        )

    @pytest.mark.asyncio
    async def test_create(self):
        credentials = await create_fake_credential()
        user = await self.repository.create(**credentials)
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_retrieve(self, user):
        result = await self.repository.retrieve(id=user.id)
        assert result.id == user.id

    @pytest.mark.asyncio
    async def test_update(self, user):
        new_first_name = "new name"
        result = await self.repository.update(user, first_name=new_first_name)
        assert result.first_name == new_first_name

    @pytest.mark.asyncio
    async def test_delete(self, user):
        result = await self.repository.delete(user)
        assert result is None

    @pytest.mark.asyncio
    async def test_list(self):
        result = await self.repository.list()
        assert result is not None

    @pytest.mark.asyncio
    async def test_empty_list(self):
        result = await self.repository.list()
        assert not result
