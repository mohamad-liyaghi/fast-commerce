import pytest
from uuid import uuid4
from src.app.repositories import CartRepository
from src.core.exceptions import (
    CartItemOwnerException,
    CartItemQuantityException,
    CartItemNotFound,
)


class TestAuthRepository:
    @pytest.fixture(autouse=True)
    def setup(self, get_test_db, get_test_redis, product):
        self.repository = CartRepository(redis_client=get_test_redis)
        self.product = product
        self.data = {
            "product_uuid": str(self.product.uuid),
            "quantity": 1,
        }

    @pytest.mark.asyncio
    async def test_add_item_to_cart(self, admin):
        await self.repository.add_item(
            product=self.product, request_user=admin, **self.data
        )

    @pytest.mark.asyncio
    async def test_add_item_by_product_owner_fails(self, user):
        with pytest.raises(CartItemOwnerException):
            await self.repository.add_item(
                product=self.product, request_user=user, **self.data
            )

    @pytest.mark.asyncio
    async def test_add_more_than_10_items_fails(self, admin):
        self.data["quantity"] = 10
        with pytest.raises(CartItemQuantityException):
            await self.repository.add_item(
                product=self.product, request_user=admin, **self.data
            )

    @pytest.mark.asyncio
    async def test_update_item(self, admin):
        await self.repository.add_item(
            product=self.product, request_user=admin, **self.data
        )
        self.data["quantity"] = 2
        await self.repository.update_item(
            request_user=admin, product_uuid=self.product.uuid, quantity=5
        )

    @pytest.mark.asyncio
    async def test_update_non_existing_item(self, admin):
        with pytest.raises(CartItemNotFound):
            await self.repository.update_item(
                request_user=admin, product_uuid=uuid4(), quantity=5
            )

    @pytest.mark.asyncio
    async def test_delete_item(self, admin):
        await self.repository.delete_item(
            request_user=admin, product_uuid=self.product.uuid
        )

    @pytest.mark.asyncio
    async def test_delete_non_existing_item(self, admin):
        with pytest.raises(CartItemNotFound):
            await self.repository.delete_item(
                request_user=admin, product_uuid=self.product.uuid
            )
