import pytest
from tests.utils.faker import create_fake_credential
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
        self.repository = AuthRepository(
            model=User, database_session=get_test_db, redis_session=get_test_redis
        )

    @pytest.mark.asyncio
    async def test_register(self):
        """
        When user registers, it creates a new user in the database
        """
        credential = await create_fake_credential()
        user = await self.repository.register(data=credential)
        assert user.get("email") == credential.get("email")

    @pytest.mark.asyncio
    async def test_register_duplicate_user(self, user):
        """
        When user registers a duplicate user, it raises an exception
        """
        credential = await create_fake_credential()
        credential["email"] = user.email
        with pytest.raises(UserAlreadyExistError):
            await self.repository.register(data=credential)

    @pytest.mark.asyncio
    async def test_register_pending_user(self, cached_user):
        """
        When user registers a pending user, it raises an exception
        """
        credential = await create_fake_credential()
        credential["email"] = cached_user.get("email")
        with pytest.raises(UserPendingVerificationError):
            await self.repository.register(data=credential)

    @pytest.mark.asyncio
    async def test_verify(self, cached_user):
        """
        When user verifies its account, it marks the user as verified
        """
        email = cached_user.get("email")
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=cached_user.get("email")
        )
        cached_user = await self.redis.hgetall(cache_key)
        await self.repository.verify(email=email, otp=cached_user.get("otp"))
        user = await self.repository.retrieve(email=email)

        assert user

    @pytest.mark.asyncio
    async def test_verify_duplicate_user(self, user):
        """
        When user verifies a duplicate user, it raises an exception
        """
        email = user.email
        otp = "1234"
        with pytest.raises(UserAlreadyExistError):
            await self.repository.verify(email=email, otp=otp)

    @pytest.mark.asyncio
    async def test_verify_invalid_otp(self, cached_user):
        """
        When user verifies an invalid OTP, it raises an exception
        """
        email = cached_user.get("email")
        otp = 12  # Credentials are  5 digits long
        with pytest.raises(InvalidVerificationCodeError):
            await self.repository.verify(email=email, otp=otp)

    @pytest.mark.asyncio
    async def test_login(self, user):
        """
        When user logs in, it returns a user object
        """
        email = user.email
        password = "1234"
        await self.repository.update(user, password=password)

        result = await self.repository.login(email=email, password=password)

        assert result

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, user):
        """
        When user logs in with invalid credentials, it raises an exception
        """
        email = user.email
        password = "1234"
        with pytest.raises(InvalidCredentialsError):
            await self.repository.login(email=email, password=password)

    @pytest.mark.asyncio
    async def test_login_invalid_user(self):
        """
        When user logs in with invalid user, it raises an exception
        """
        email = "not@exist.com"
        password = "1234"
        with pytest.raises(UserNotFoundError):
            await self.repository.login(email=email, password=password)
