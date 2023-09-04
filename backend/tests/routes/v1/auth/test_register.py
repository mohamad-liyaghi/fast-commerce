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
        """Test user creation."""
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_register_user_no_data(self) -> None:
        """Test user creation."""
        response = await self.client.post(self.url)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_register_existing_email(self, user):
        self.data["email"] = user.email
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_register_pending_verification(self):
        # Create a user
        await self.client.post(self.url, json=self.data)
        # Create again
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
