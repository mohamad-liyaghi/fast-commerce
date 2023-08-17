import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRegisterRoute:

    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient) -> None:
        self.data = {
            "email": "fake@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password",
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
        self.data['email'] = user.email
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_register_pending_verification(self):
        # Create a user
        await self.client.post(self.url, json=self.data)
        # Create again
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
