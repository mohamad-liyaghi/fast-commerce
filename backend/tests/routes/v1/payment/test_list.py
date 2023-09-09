from fastapi import status
import pytest


class TestPaymentListRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/payment/"

    @pytest.mark.asyncio
    async def test_pay_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_empty_list(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_get_list(self, admin_client, payment):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
