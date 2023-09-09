import pytest
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPaymentProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, payment) -> None:
        self.url = f"v1/payment/{payment.uuid}"
        self.payment = payment

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve_by_non_owner(self, authorized_client, user):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert user.id != self.payment.user_id

    @pytest.mark.asyncio
    async def test_retrieve_by_owner(self, admin_client, admin):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
        assert self.payment.user_id == admin.id

    @pytest.mark.asyncio
    async def test_retrieve_not_found(self, admin_client):
        url = f"v1/payment/{uuid4()}"
        response = await admin_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
