from .auth import UserRegisterIn, UserVerifyIn, UserLoginIn
from .profile import ProfileUpdateIn
from .vendor import VendorCreateIn, VendorUpdateStatusIn, VendorUpdateIn
from .product import ProductCreateIn, ProductUpdateIn
from .cart import CartAddIn, CartUpdateIn
from .order import OrderCreateIn, OrderStatusIn
from .order_item import OrderItemStatusIn

auth = [
    "UserRegisterIn",
    "UserVerifyIn",
    "UserLoginIn",
]

profile = [
    "ProfileUpdateIn",
]

vendor = [
    "VendorCreateIn",
    "VendorUpdateStatusIn",
    "VendorUpdateIn",
]


product = [
    "ProductCreateIn",
    "ProductUpdateIn",
]

cart = [
    "CartAddIn",
    "CartUpdateIn",
]

order = [
    "OrderCreateIn",
    "OrderStatusIn",
]

order_item = [
    "OrderItemStatusIn",
]

__all__ = auth + profile + vendor + product + cart + order + order_item
