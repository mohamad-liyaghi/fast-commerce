import pytest
from uuid import uuid4
from fastapi import status


@pytest.mark.asyncio
class TestRetrieveOrderRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, order) -> None:
        self.url = f"v1/order/{order.uuid}"

    @pytest.mark.asyncio
    async def test_retrieve(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve_with_non_owner(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_retrieve_with_owner(self, admin_client):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_retrieve_not_found(self, admin_client):
        response = await admin_client.get(f"v1/order/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
