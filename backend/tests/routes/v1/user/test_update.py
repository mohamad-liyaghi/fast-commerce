import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUpdateProfileRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, user) -> None:
        self.client = client
        self.url = f"v1/user/{user.uuid}"
        self.data = {
            "first_name": "updated first name",
            "last_name": "updated last name",
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized(self) -> None:
        response = await self.client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update(self, authorized_client) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_another_user(self, authorized_client, admin) -> None:
        response = await authorized_client.put(f"v1/user/{admin.uuid}", json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
