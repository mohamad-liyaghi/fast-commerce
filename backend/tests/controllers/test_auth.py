import pytest
from fastapi import HTTPException
from tests.utils import create_fake_credential


class TestAuthController:

    @pytest.mark.asyncio
    async def test_register(self, auth_controller):
        await auth_controller.register(create_fake_credential())

    @pytest.mark.asyncio
    async def test_register_already_exists(self, auth_controller, user):
        credential = create_fake_credential()
        credential['email'] = user.email
        with pytest.raises(HTTPException):
            await auth_controller.register(credential)

    @pytest.mark.asyncio
    async def test_register_exists_in_cache(self, auth_controller, cached_user):
        credential = create_fake_credential()
        credential['email'] = cached_user['email']
        with pytest.raises(HTTPException):
            await auth_controller.register(credential)

    @pytest.mark.asyncio
    async def test_verify(self, auth_controller, cached_user, get_test_redis):
        cached_user = await get_test_redis.hgetall(cached_user['email'])
        otp = cached_user['otp']
        await auth_controller.verify(email=cached_user['email'], otp=otp)

    @pytest.mark.asyncio
    async def test_verify_invalid_coed(self, auth_controller, cached_user, get_test_redis):
        cached_user = await get_test_redis.hgetall(cached_user['email'])
        invalid_otp = int(cached_user['otp']) + 10
        with pytest.raises(HTTPException):
            await auth_controller.verify(
                email=cached_user['email'],
                otp=invalid_otp
            )

    @pytest.mark.asyncio
    async def test_verify_active_user(self, auth_controller, user):
        with pytest.raises(HTTPException):
            await auth_controller.verify(email=user.email, otp=12345)

    @pytest.mark.asyncio
    async def test_verify_not_exist(self, auth_controller):
        with pytest.raises(HTTPException):
            await auth_controller.verify(email='not@exist.com', otp=12345)