import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from tests.utils.faker import create_fake_credential


@pytest.mark.asyncio
class TestRegisterRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient) -> None:
        credential = await create_fake_credential()
        self.data = {
            "email": credential["email"],
            "first_name": credential["first_name"],
            "last_name": credential["last_name"],
            "password": credential["password"],
        }
        self.client = client
        self.url = "v1/auth/register"

    @pytest.mark.asyncio
    async def test_register_user(self) -> None:
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_register_user_invalid_data(self) -> None:
        response = await self.client.post(self.url)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_register_user_exists(self, user):
        self.data["email"] = user.email
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_register_user_pending_verification(self):
        await self.client.post(self.url, json=self.data)  # Register once
        response = await self.client.post(self.url, json=self.data)  # Register again
        assert response.status_code == status.HTTP_400_BAD_REQUEST
