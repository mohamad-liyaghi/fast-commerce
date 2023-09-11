import pytest
from src.app.enums import OrderItemStatusEnum
from src.core.exceptions import (
    AdminRequiredException,
    VendorRequiredException,
    InappropriateOrderStatus,
)
from src.core.exceptions import CartEmptyException
from src.app.enums import OrderStatusEnum
from src.core.exceptions import OrderAlreadyPaid


class TestOrderItemRepository:
    @pytest.fixture(autouse=True)
    def setup(self, order_item_controller):
        self.repository = order_item_controller.repository

    @pytest.mark.asyncio
    async def test_set_delivering(self, preparing_order_item, user):
        await self.repository.set_delivering(preparing_order_item, user)
        assert preparing_order_item.status == OrderItemStatusEnum.DELIVERING

    @pytest.mark.asyncio
    async def test_set_delivering_non_vendor(self, preparing_order_item, admin):
        with pytest.raises(VendorRequiredException):
            await self.repository.set_delivering(preparing_order_item, admin)

    @pytest.mark.asyncio
    async def test_set_delivering_delivered_item(self, delivered_order_item, user):
        with pytest.raises(InappropriateOrderStatus):
            await self.repository.set_delivering(delivered_order_item, user)

    @pytest.mark.asyncio
    async def test_set_delivered(self, delivering_order_item, admin):
        await self.repository.set_delivered(delivering_order_item, admin)
        assert delivering_order_item.status == OrderItemStatusEnum.DELIVERED

    @pytest.mark.asyncio
    async def test_set_delivered_non_admin(self, delivering_order_item, user):
        with pytest.raises(AdminRequiredException):
            await self.repository.set_delivered(delivering_order_item, user)

    @pytest.mark.asyncio
    async def test_set_delivered_preparing_item(self, preparing_order_item, admin):
        with pytest.raises(InappropriateOrderStatus):
            await self.repository.set_delivered(preparing_order_item, admin)
