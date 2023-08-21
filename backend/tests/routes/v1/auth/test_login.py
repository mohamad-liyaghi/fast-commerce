import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestLoginRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, user) -> None:
        self.user = user
        self.data = {"email": user.email, "password": "default"}
        self.client = client
        self.url = "v1/auth/login"

    @pytest.mark.asyncio
    async def test_login(self, get_test_db, user_controller) -> None:
        password = "1234"
        await user_controller.repository.update(self.user, password=password)
        self.data["password"] = password
        await get_test_db.refresh(self.user)
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_login_invalid_password(self) -> None:
        self.data["password"] = "Invalid Password"
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_login_invalid_data(self) -> None:
        response = await self.client.post(self.url)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_login_user_not_exist(self) -> None:
        self.data["email"] = self.data["email"] + "string"
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_login_user_cached(self, cached_user) -> None:
        self.data["email"] = cached_user["email"]
        self.data["password"] = cached_user["password"]
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
