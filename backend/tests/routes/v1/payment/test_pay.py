from fastapi import status
import pytest


class TestPayOrderRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, order) -> None:
        self.url = f"v1/payment/{order.uuid}"
        self.order = order

    @pytest.mark.asyncio
    async def test_pay_unauthorized(self, client):
        response = await client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_pay_by_other_user(self, authorized_client, user):
        response = await authorized_client.post(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert self.order.user_id != user.id

    @pytest.mark.asyncio
    async def test_pay_order(self, admin_client, admin):
        response = await admin_client.post(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert self.order.user_id == admin.id

    @pytest.mark.asyncio
    async def test_pay_order_twice(self, admin_client, payment):
        response = await admin_client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
