from .auth import UserRegisterIn, UserVerifyIn, UserLoginIn
from .profile import ProfileUpdateIn
from .vendor import VendorCreateIn, VendorUpdateStatusIn, VendorUpdateIn
from .product import ProductCreateIn, ProductUpdateIn

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

__all__ = auth + profile + vendor + product
