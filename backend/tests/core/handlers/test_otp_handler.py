import pytest
from src.core.handlers import OtpHandler


class TestOtpHandler:
    @pytest.mark.asyncio
    async def test_create_otp(self):
        otp = await OtpHandler.create()
        assert len(str(otp)) == 5
