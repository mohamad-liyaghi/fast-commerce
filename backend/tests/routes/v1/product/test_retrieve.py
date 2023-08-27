import pytest
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRetrieveProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, product) -> None:
        self.client = client
        self.url = f"v1/product/{product.uuid}"

    @pytest.mark.asyncio
    async def test_retrieve(self):
        response = await self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_retrieve_not_found(self):
        url = f"v1/product/{uuid4()}"
        response = await self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
