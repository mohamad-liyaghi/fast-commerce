import pytest
import asyncio
from tests.utils.faker import create_fake_credential, USER_PASSWORD
from src.app.repositories import AuthRepository
from src.app.models import User
from src.core.configs import settings
from src.core.utils import format_key
from src.core.exceptions import (
    UserAlreadyExistError,
    UserPendingVerificationError,
    UserNotFoundError,
    InvalidVerificationCodeError,
    InvalidCredentialsError,
)


class TestAuthRepository:
    @pytest.fixture(autouse=True)
    def setup(self, get_test_db, get_test_redis):
        self.redis = get_test_redis
        self.credentials = asyncio.run(create_fake_credential())
        self.repository = AuthRepository(
            model=User, database_session=get_test_db, redis_session=get_test_redis
        )

    @pytest.mark.asyncio
    async def test_register_with_valid_data(self):
        user = await self.repository.register_user(data=self.credentials)
        assert user.get("email") == self.credentials.get("email")

    @pytest.mark.asyncio
    async def test_register_user_already_exists(self, user):
        self.credentials["email"] = user.email

        with pytest.raises(UserAlreadyExistError):
            await self.repository.register_user(data=self.credentials)

    @pytest.mark.asyncio
    async def test_register_user_pending_verification(self, cached_user):
        self.credentials["email"] = cached_user.get("email")

        with pytest.raises(UserPendingVerificationError):
            await self.repository.register_user(data=self.credentials)

    @pytest.mark.asyncio
    async def test_verify_with_invalid_otp(self, cached_user):
        email = cached_user.get("email")
        otp = 12  # Credentials are  5 digits long
        with pytest.raises(InvalidVerificationCodeError):
            await self.repository.verify_user(email=email, otp=otp)

    @pytest.mark.asyncio
    async def test_verify_valid_otp(self, cached_user):
        email = cached_user.get("email")
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=cached_user.get("email")
        )
        cached_user = await self.redis.hgetall(cache_key)

        await self.repository.verify_user(email=email, otp=cached_user.get("otp"))
        assert await self.repository.retrieve(email=email)

    @pytest.mark.asyncio
    async def test_verify_already_verified(self, user):
        email = user.email
        otp = 1234
        with pytest.raises(UserAlreadyExistError):
            await self.repository.verify_user(email=email, otp=otp)

    @pytest.mark.asyncio
    async def test_login_valid_credentials(self, user):
        email = user.email
        result = await self.repository.login_user(email=email, password=USER_PASSWORD)

        assert result

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, user):
        email = user.email
        password = user.password[:3]
        with pytest.raises(InvalidCredentialsError):
            await self.repository.login_user(email=email, password=password)

    @pytest.mark.asyncio
    async def test_login_user_not_exist(self):
        email = "not@exist.com"
        password = "1234"
        with pytest.raises(UserNotFoundError):
            await self.repository.login_user(email=email, password=password)
