from .auth import UserRegisterIn, UserVerifyIn, UserLoginIn
from .profile import ProfileUpdateIn
from .vendor import VendorCreateIn, VendorUpdateStatusIn, VendorUpdateIn
from .product import ProductCreateIn, ProductUpdateIn
from .cart import CartAddIn, CartUpdateIn
from .order import OrderCreateIn

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
]


__all__ = auth + profile + vendor + product + cart + order
