from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHandler:
    """
    This handler is responsible for hashing and verifying passwords.
    """

    @staticmethod
    async def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return context.hash(password)

    @staticmethod
    async def verify_password(hashed_password: str, password: str) -> bool:
        """Verify password using bcrypt"""
        return context.verify(password, hashed_password)
