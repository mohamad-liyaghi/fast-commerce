from datetime import datetime, timedelta
from jose import jwt
from src.core.configs import settings


class JWTHandler:
    @staticmethod
    async def create_access_token(data: dict):
        """
        Create a new access token.
        """
        to_encode = data.copy()

        expire_at = datetime.utcnow() + timedelta(settings.JWT_EXPIRATION_MINUETS)
        to_encode.update({"exp": expire_at, "user_uuid": data.get("user_uuid")})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
