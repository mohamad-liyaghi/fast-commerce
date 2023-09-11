import pytest
from src.core.exceptions import CartEmptyException
from src.app.enums import OrderStatusEnum
from src.core.exceptions import OrderAlreadyPaid


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
    async def test_create_empty_cart(self):
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
    async def test_order_price(self, product):
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
    async def test_set_paid(self, order):
        order = await self.repository.set_paid(order=order)
        assert order.status == OrderStatusEnum.PREPARING

    @pytest.mark.asyncio
    async def test_set_paid_twice(self, order):
        order = await self.repository.set_paid(order=order)
        with pytest.raises(OrderAlreadyPaid):
            await self.repository.set_paid(order=order)
