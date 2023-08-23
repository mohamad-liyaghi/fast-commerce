from .auth import UserRegisterIn, UserVerifyIn, UserLoginIn
from .profile import ProfileUpdateIn
from .vendor import VendorCreateIn, VendorUpdateStatusIn, VendorUpdateIn

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


__all__ = [
    *auth,
    *profile,
    *vendor,
]
