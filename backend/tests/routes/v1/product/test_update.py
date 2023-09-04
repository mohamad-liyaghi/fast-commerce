from fastapi import status
from uuid import uuid4
import pytest
from tests.utils.faker import create_product_credential


class TestUpdateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, product) -> None:
        self.url = f"v1/product/{product.uuid}"
        self.product = product

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client) -> None:
        credential = await create_product_credential()
        response = await client.put(self.url, json=credential)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_other_user(self, admin_client, admin) -> None:
        credential = await create_product_credential()
        response = await admin_client.put(self.url, json=credential)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert admin != self.product.user_id

    @pytest.mark.asyncio
    async def test_update_by_vendor(self, authorized_client, user):
        credential = await create_product_credential()
        response = await authorized_client.put(self.url, json=credential)
        assert response.status_code == status.HTTP_200_OK
        assert user.id == self.product.user_id

    @pytest.mark.asyncio
    async def test_update_not_found(self, authorized_client):
        credential = await create_product_credential()
        url = f"v1/product/{uuid4()}"
        response = await authorized_client.put(url, json=credential)
        assert response.status_code == status.HTTP_404_NOT_FOUND
