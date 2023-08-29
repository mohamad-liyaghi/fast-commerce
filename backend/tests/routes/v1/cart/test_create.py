from fastapi import status
import json
from src.core.utils import format_key
from src.core.configs import settings
import pytest
from uuid import uuid4


class TestAddCartItemRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, product) -> None:
        self.url = f"v1/cart/"
        self.product = product
        self.data = {
            "product_uuid": str(self.product.uuid),
            "quantity": 1,
        }

    @pytest.mark.asyncio
    async def test_add_unauthorized(self, client):
        response = await client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_add_item_by_product_user(self, authorized_client, user):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.product.user_id == user.id

    @pytest.mark.asyncio
    async def test_add_item(self, admin_client, admin):
        response = await admin_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.product.user_id != admin.id

    @pytest.mark.asyncio
    async def test_add_item_increment_quantity(
        self, admin_client, cart_controller, admin, cart
    ):
        response = await admin_client.post(self.url, json=self.data)
        cache_key = await format_key(key=settings.CACHE_CART_KEY, user_uuid=admin.uuid)
        cart_product = await cart_controller.get_cache(
            key=cache_key, field=str(self.product.uuid)
        )
        cart_product = json.loads(cart_product)

        assert response.status_code == status.HTTP_201_CREATED
        assert cart["quantity"] == 1
        assert cart_product["quantity"] == 2

    @pytest.mark.asyncio
    async def test_add_item_not_found(self, admin_client, admin):
        self.data["product_uuid"] = str(uuid4())
        response = await admin_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
