import pytest
from tests.utils.mocking import create_fake_credential
from src.app.repositories import UserRepository
from src.app.models import User


class TestBaseRepository:
    @pytest.fixture(autouse=True)
    def setup(self, get_test_db, get_test_redis):
        self.repository = UserRepository(
            model=User, database_session=get_test_db, redis_session=get_test_redis
        )

    @pytest.mark.asyncio
    async def test_list_password_is_hashed(self):
        credential = await create_fake_credential()
        password = credential.get("password")

        user = await self.repository.create(**credential)
        assert user.password != password

    @pytest.mark.asyncio
    async def test_update_password(self, user):
        """
        When user updates its password, the new pass gets hashed
        """
        password = "1234"
        result = await self.repository.update(user, password=password)

        assert not result.password == password
