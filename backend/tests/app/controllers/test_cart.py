import pytest
import uuid
from fastapi import HTTPException


class TestCartController:
    @pytest.fixture(autouse=True)
    def setup(self, cart_controller, product):
        self.controller = cart_controller
        self.data = {
            "product_uuid": str(product.uuid),
            "quantity": 1,
        }

    @pytest.mark.asyncio
    async def test_add_item(self, admin, product_controller):
        await self.controller.add_item(
            product_controller=product_controller, request_user=admin, **self.data
        )

    @pytest.mark.asyncio
    async def test_add_by_product_owner(self, user, product_controller):
        with pytest.raises(HTTPException):
            await self.controller.add_item(
                product_controller=product_controller, request_user=user, **self.data
            )

    @pytest.mark.asyncio
    async def test_add_more_than_10_items(self, admin, product_controller):
        self.data["quantity"] = 10
        await self.controller.add_item(
            product_controller=product_controller, request_user=admin, **self.data
        )
        self.data["quantity"] = 1
        with pytest.raises(HTTPException):
            await self.controller.add_item(
                product_controller=product_controller, request_user=admin, **self.data
            )

    @pytest.mark.asyncio
    async def test_get_items_empty(self, admin):
        items = await self.controller.get_items(request_user=admin)
        assert not items

    @pytest.mark.asyncio
    async def test_get_items(self, admin, cart):
        items = await self.controller.get_items(request_user=admin)
        assert items is not None

    @pytest.mark.asyncio
    async def test_update_item(self, admin, cart):
        await self.controller.update_item(
            request_user=admin, product_uuid=self.data["product_uuid"], quantity=5
        )

    @pytest.mark.asyncio
    async def test_update_item_not_found(self, admin):
        with pytest.raises(HTTPException):
            await self.controller.update_item(
                request_user=admin, product_uuid=uuid.uuid4(), quantity=5
            )

    @pytest.mark.asyncio
    async def test_delete_item(self, admin, cart):
        await self.controller.delete_item(
            request_user=admin, product_uuid=self.data["product_uuid"]
        )

    @pytest.mark.asyncio
    async def test_delete_item_not_found(self, admin):
        with pytest.raises(HTTPException):
            await self.controller.delete_item(
                request_user=admin, product_uuid=uuid.uuid4()
            )
