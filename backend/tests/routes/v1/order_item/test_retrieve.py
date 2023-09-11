import pytest
from uuid import uuid4
from fastapi import status


@pytest.mark.asyncio
class TestRetrieveOrderItemRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, preparing_order_item) -> None:
        self.url = f"v1/order_item/{preparing_order_item.uuid}"
        self.order_item = preparing_order_item

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve_by_admin(self, admin_client, admin):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert admin.is_admin

    @pytest.mark.asyncio
    async def test_retrieve_by_order_user(self, admin_client, admin):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert self.order_item.order.user_id == admin.id

    async def test_retrieve_by_vendor(self, accepted_vendor, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert self.order_item.vendor_id == accepted_vendor.id

    @pytest.mark.asyncio
    async def test_retrieve_not_found(self, admin_client):
        url = f"v1/order_item/{uuid4()}"
        response = await admin_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
