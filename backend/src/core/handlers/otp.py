from random import randint


class OtpHandler:
    """
    This handler is responsible for creating and verifying otp codes.
    """

    @staticmethod
    async def create() -> int:
        """Hash password using bcrypt"""
        return randint(11111, 99999)

    # @staticmethod
    # async def verify(hashed_password: str, password: str) -> bool:
