import pytest
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
    async def test_add_item(self, admin):
        await self.repository.add_item(
            product=self.product, request_user=admin, **self.data
        )

    @pytest.mark.asyncio
    async def test_add_by_product_owner(self, user):
        with pytest.raises(CartItemOwnerException):
            await self.repository.add_item(
                product=self.product, request_user=user, **self.data
            )

    @pytest.mark.asyncio
    async def test_add_more_than_10_items(self, admin):
        self.data["quantity"] = 10
        await self.repository.add_item(
            product=self.product, request_user=admin, **self.data
        )
        self.data["quantity"] = 1
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
    async def test_update_item_not_found(self, admin):
        with pytest.raises(CartItemNotFound):
            await self.repository.update_item(
                request_user=admin, product_uuid=self.product.uuid, quantity=5
            )

    @pytest.mark.asyncio
    async def test_delete_item(self, admin, cart):
        await self.repository.delete_item(
            request_user=admin, product_uuid=self.product.uuid
        )

    @pytest.mark.asyncio
    async def test_delete_item_not_found(self, admin):
        with pytest.raises(CartItemNotFound):
            await self.repository.delete_item(
                request_user=admin, product_uuid=self.product.uuid
            )
