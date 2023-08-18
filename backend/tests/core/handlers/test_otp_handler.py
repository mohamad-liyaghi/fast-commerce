import pytest
from src.core.handlers import OtpHandler


class TestOtpHandler:
    @pytest.mark.asyncio
    async def test_create_otp(self):
        otp = await OtpHandler.create()
        assert len(str(otp)) == 5

    @pytest.mark.asyncio
    async def test_validate(self, get_test_redis, cached_user):
        otp = await get_test_redis.hgetall(cached_user['email'])
        otp = otp['otp']
        cached_user['otp'] = otp
        assert await OtpHandler.validate(otp, cached_user)

    @pytest.mark.asyncio
    async def test_not_validate_invalid(self, get_test_redis, cached_user):
        otp = await get_test_redis.hgetall(cached_user['email'])
        otp = otp['otp']
        fake_otp = int(otp) + 10
        cached_user['otp'] = otp
        assert not await OtpHandler.validate(fake_otp, cached_user)
