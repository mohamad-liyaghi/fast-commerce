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
    async def test_get_empty_list_of_items(self, admin):
        items = await self.controller.get_items(request_user=admin)
        assert not items

    @pytest.mark.asyncio
    async def test_add_item_into_cart(self, admin, product_controller):
        await self.controller.add_item(
            product_controller=product_controller, request_user=admin, **self.data
        )

    @pytest.mark.asyncio
    async def test_add_item_by_product_owner_fails(self, user, product_controller):
        with pytest.raises(HTTPException):
            await self.controller.add_item(
                product_controller=product_controller, request_user=user, **self.data
            )

    @pytest.mark.asyncio
    async def test_add_more_than_10_items_fails(self, admin, product_controller):
        self.data["quantity"] = 10
        with pytest.raises(HTTPException):
            await self.controller.add_item(
                product_controller=product_controller, request_user=admin, **self.data
            )

    @pytest.mark.asyncio
    async def test_get_list_of_items(self, admin):
        items = await self.controller.get_items(request_user=admin)
        assert items is not None

    @pytest.mark.asyncio
    async def test_update_item(self, admin):
        await self.controller.update_item(
            request_user=admin, product_uuid=self.data["product_uuid"], quantity=5
        )

    @pytest.mark.asyncio
    async def test_update_non_existing_item(self, admin):
        with pytest.raises(HTTPException):
            await self.controller.update_item(
                request_user=admin, product_uuid=uuid.uuid4(), quantity=5
            )

    @pytest.mark.asyncio
    async def test_delete_item(self, admin):
        await self.controller.delete_item(
            request_user=admin, product_uuid=self.data["product_uuid"]
        )

    @pytest.mark.asyncio
    async def test_delete_non_existing_item(self, admin):
        with pytest.raises(HTTPException):
            await self.controller.delete_item(
                request_user=admin, product_uuid=uuid.uuid4()
            )
