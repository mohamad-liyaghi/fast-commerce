import pytest
from src.core.handlers import OtpHandler
from src.core.utils import format_key
from src.core.config import settings


class TestOtpHandler:
    @pytest.mark.asyncio
    async def test_create_otp(self):
        otp = await OtpHandler.create()
        assert len(str(otp)) == 5

    @pytest.mark.asyncio
    async def test_validate(self, get_test_redis, cached_user):
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY,
            email=cached_user['email']
        )
        otp = await get_test_redis.hgetall(cache_key)
        otp = otp['otp']
        cached_user['otp'] = otp
        assert await OtpHandler.validate(otp, cached_user)

    @pytest.mark.asyncio
    async def test_not_validate_invalid(self, get_test_redis, cached_user):
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY,
            email=cached_user['email']
        )
        otp = await get_test_redis.hgetall(cache_key)
        otp = otp['otp']
        fake_otp = int(otp) + 10
        cached_user['otp'] = otp
        assert not await OtpHandler.validate(fake_otp, cached_user)
