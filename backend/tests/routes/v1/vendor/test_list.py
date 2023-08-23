import pytest
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestListVendorRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/vendor/"

    @pytest.mark.asyncio
    async def test_list_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_list_empty(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_list(self, authorized_client, accepted_vendor):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None