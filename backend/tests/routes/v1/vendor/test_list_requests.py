import pytest
from fastapi import status
from src.app.models import VendorStatus


@pytest.mark.asyncio
class TestListVendorRequestRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = "v1/vendor/requests/"

    @pytest.mark.asyncio
    async def test_list_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_list_by_non_admin(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_list_by_admin_empty(self, admin_client):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_list_by_admin(self, admin_client, pending_vendor):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
        assert len(response.json()) == 1
        assert str(pending_vendor.uuid) == response.json()[0]["uuid"]

    @pytest.mark.asyncio
    async def test_list_by_admin_with_params(self, admin_client, accepted_vendor):
        response = await admin_client.get(
            self.url + f"?status={VendorStatus.ACCEPTED.value}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
        assert len(response.json()) == 1
        assert str(accepted_vendor.uuid) == response.json()[0]["uuid"]
