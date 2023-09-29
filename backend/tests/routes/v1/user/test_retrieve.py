import pytest
from fastapi import status
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
class TestRetrieveProfileRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, user) -> None:
        self.client = client
        self.url = f"v1/user/{user.uuid}"

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized(self) -> None:
        response = await self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve_existing_user(self, authorized_client) -> None:
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_retrieve_non_existing_user(self, authorized_client) -> None:
        url = f"v1/user/{uuid4()}"
        response = await authorized_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
