import pytest
from fastapi import status
from httpx import AsyncClient
from src.core.utils import format_key
from src.core.configs import settings


@pytest.mark.asyncio
class TestVerifyRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, cached_user) -> None:
        self.client = client
        self.data = {"email": cached_user["email"], "otp": ...}
        self.url = "v1/auth/verify"

    @pytest.mark.asyncio
    async def test_verify(self, get_test_redis) -> None:
        """Test user creation."""
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=self.data["email"]
        )
        cached_user = await get_test_redis.hgetall(cache_key)
        self.data["otp"] = cached_user["otp"]
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_verify_invalid_code(self, get_test_redis) -> None:
        cache_key = await format_key(
            key=settings.CACHE_USER_KEY, email=self.data["email"]
        )
        cached_user = await get_test_redis.hgetall(cache_key)
        self.data["otp"] = int(cached_user["otp"]) - 2  # Invalid code
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_verify_invalid_data(self) -> None:
        response = await self.client.post(self.url)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_verify_invalid_user(self) -> None:
        self.data["otp"] = 12345
        self.data["email"] = "not@exist.com"
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_verify_not_found(self) -> None:
        self.data["email"] = "non@gmail.com"
        self.data["otp"] = 12345
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_verify_active_user(self, user) -> None:
        self.data["otp"] = 12345
        self.data["email"] = user.email
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_verify_long_conde(self) -> None:
        self.data["otp"] = 1234567
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
