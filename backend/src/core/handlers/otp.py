from random import randint


class OtpHandler:
    """
    This handler is responsible for creating and verifying otp codes.
    """

    @staticmethod
    async def create() -> int:
        """Hash password using bcrypt"""
        return randint(11111, 99999)

    @staticmethod
    async def validate(otp: str, user: dict) -> bool:
        """Validate otp code"""
        user_otp = user.get('otp')
        return int(otp) == int(user_otp)
