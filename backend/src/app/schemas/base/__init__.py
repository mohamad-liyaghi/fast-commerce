from .user import UserBaseEmail, UserBasePassword, UserBase, CurrentUser
from .vendor import VendorBase, VendorBaseOut
from .product import BaseProduct, BaseProductCreate

vendors = [
    "VendorBase",
    "VendorBaseOut",
]

users = [
    "UserBaseEmail",
    "UserBasePassword",
    "UserBase",
    "CurrentUser",
]

products = [
    "BaseProduct",
    "BaseProductCreate",
]

__all__ = vendors + users + products
