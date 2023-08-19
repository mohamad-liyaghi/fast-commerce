import pytest
import pytest_asyncio
from src.core.handlers import PasswordHandler


class TestPasswordHandler:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        self.password = 'password'

    @pytest.mark.asyncio
    async def test_hash_password(self):
        hashed_password = await PasswordHandler.hash_password(self.password)
        assert hashed_password != self.password

    @pytest.mark.asyncio
    async def test_verify_password(self):
        hashed_password = await PasswordHandler.hash_password(self.password)
        assert await PasswordHandler.verify_password(
            hashed_password, self.password
        )

    @pytest.mark.asyncio
    async def test_not_verify_invalid_password(self):
        hashed_password = await PasswordHandler.hash_password(self.password)
        assert not await PasswordHandler.verify_password(
            hashed_password, 'fake pass'
        )
