import pytest
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRetrieveVendorRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, accepted_vendor) -> None:
        self.client = client
        self.url = f"v1/vendor/{accepted_vendor.uuid}"

    @pytest.mark.asyncio
    async def test_retrieve(self):
        response = await self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_retrieve_not_found(self):
        response = await self.client.get(f"v1/vendor/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
