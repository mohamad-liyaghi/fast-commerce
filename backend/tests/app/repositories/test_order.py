import pytest
from src.core.exceptions import CartEmptyException
from src.app.enums import OrderStatusEnum
from src.core.exceptions import OrderAlreadyPaid, OrderInvalidStatus


class TestOrderRepository:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        admin,
        order_controller,
        cart,
        order_item_controller,
        cart_controller,
        product_controller,
    ):
        self.repository = order_controller.repository
        self.order_item_controller = order_item_controller
        self.cart_controller = cart_controller
        self.product_controller = product_controller
        self.cart = cart
        self.user = admin

    @pytest.mark.asyncio
    async def test_create_order(self):
        await self.repository.create_order(
            user=self.user,
            order_item_controller=self.order_item_controller,
            cart_controller=self.cart_controller,
            cart=self.cart,
            product_controller=self.product_controller,
            delivery_address="test address",
        )
        assert await self.repository.retrieve(many=True) is not None

    @pytest.mark.asyncio
    async def test_create_with_empty_cart_fails(self):
        self.cart = {}
        with pytest.raises(CartEmptyException):
            await self.repository.create_order(
                user=self.user,
                order_item_controller=self.order_item_controller,
                cart_controller=self.cart_controller,
                cart=self.cart,
                product_controller=self.product_controller,
                delivery_address="test address",
            )

    @pytest.mark.asyncio
    async def test_set_order_total_price(self, product):
        order = await self.repository.create_order(
            user=self.user,
            order_item_controller=self.order_item_controller,
            cart_controller=self.cart_controller,
            cart=self.cart,
            product_controller=self.product_controller,
            delivery_address="test address",
        )

        assert order.total_price == product.price

    @pytest.mark.asyncio
    async def test_set_pending_order_to_delivering_fails(self, order):
        with pytest.raises(OrderInvalidStatus):
            await self.repository.set_delivering(order=order)

    @pytest.mark.asyncio
    async def test_set_paid(self, order):
        order = await self.repository.set_paid(order=order)
        assert order.status == OrderStatusEnum.PREPARING

    @pytest.mark.asyncio
    async def test_set_paid_twice(self, paid_order):
        with pytest.raises(OrderAlreadyPaid):
            await self.repository.set_paid(order=paid_order)

    @pytest.mark.asyncio
    async def test_set_delivering(self, paid_order):
        updated_order = await self.repository.set_delivering(order=paid_order)
        assert updated_order.status == OrderStatusEnum.DELIVERING

    @pytest.mark.asyncio
    async def test_set_delivered(self, delivering_order):
        updated_order = await self.repository.set_delivered(order=delivering_order)
        assert updated_order.status == OrderStatusEnum.DELIVERED

    @pytest.mark.asyncio
    async def test_set_delivered_invalid_status(self, order):
        with pytest.raises(OrderInvalidStatus):
            await self.repository.set_delivered(order=order)
