import pytest
import pytest_asyncio
from fastapi import status
from src.app.enums import OrderItemStatusEnum


@pytest.mark.asyncio
class TestRetrievePendingOrderItemRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/order_item/preparing"

    @pytest.mark.asyncio
    async def test_get_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_not_vendor(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_empty(self, authorized_client, accepted_vendor):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_get_unpaid_order(self, authorized_client, accepted_vendor, order):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_get_paid_order(self, authorized_client, accepted_vendor, paid_order):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
