from fastapi import status
import pytest
from httpx import AsyncClient


class TestListCartRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/cart/"

    @pytest.mark.asyncio
    async def test_list_unauthorized(self, client: AsyncClient) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_empty_list(self, authorized_client) -> None:
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_non_empty_list(self, cart, admin_client) -> None:
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
