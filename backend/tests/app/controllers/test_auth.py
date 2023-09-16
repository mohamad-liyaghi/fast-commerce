import pytest
from fastapi import HTTPException
from tests.utils.faker import create_fake_credential
from src.core.utils import format_key
from src.core.configs import settings


class TestAuthController:
    @pytest.mark.asyncio
    async def test_register(self, auth_controller, get_test_redis):
        credentials = await create_fake_credential()
        await auth_controller.register_user(credentials)
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=credentials["email"]
        )
        cached_user = await get_test_redis.hgetall(cache_key)
        assert cached_user["email"] == credentials["email"]

    @pytest.mark.asyncio
    async def test_register_already_exists(self, auth_controller, user):
        credential = await create_fake_credential()
        credential["email"] = user.email
        with pytest.raises(HTTPException):
            await auth_controller.register_user(credential)

    @pytest.mark.asyncio
    async def test_register_exists_in_cache(self, auth_controller, cached_user):
        credential = await create_fake_credential()
        credential["email"] = cached_user["email"]
        with pytest.raises(HTTPException):
            await auth_controller.register_user(credential)

    @pytest.mark.asyncio
    async def test_verify(self, auth_controller, cached_user, get_test_redis):
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=cached_user["email"]
        )
        cached_user = await get_test_redis.hgetall(cache_key)
        otp = cached_user["otp"]
        await auth_controller.verify_user(email=cached_user["email"], otp=otp)

    @pytest.mark.asyncio
    async def test_verify_invalid_code(
        self, auth_controller, cached_user, get_test_redis
    ):
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=cached_user["email"]
        )
        cached_user = await get_test_redis.hgetall(cache_key)
        invalid_otp = int(cached_user["otp"]) + 10
        with pytest.raises(HTTPException):
            await auth_controller.verify_user(
                email=cached_user["email"], otp=invalid_otp
            )

    @pytest.mark.asyncio
    async def test_verify_active_user(self, auth_controller, user):
        with pytest.raises(HTTPException):
            await auth_controller.verify_user(email=user.email, otp=12345)

    @pytest.mark.asyncio
    async def test_verify_not_exist(self, auth_controller):
        with pytest.raises(HTTPException):
            await auth_controller.verify_user(email="not@exist.com", otp=12345)
