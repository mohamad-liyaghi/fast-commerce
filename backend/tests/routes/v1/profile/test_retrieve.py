import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRetrieveProfileRoute:

    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient) -> None:
        self.client = client
        self.url = "v1/profile/me"

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized(self) -> None:
        response = await self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve(self, authorized_client) -> None:
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
