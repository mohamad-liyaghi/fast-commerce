from .user import (
    UserAlreadyExistError,
    UserPendingVerificationError,
    UserNotFoundError,
    InvalidVerificationCodeError,
    InvalidCredentialsError,
)

from .vendor import (
    PendingVendorExistsException,
    RejectedVendorExistsException,
    AcceptedVendorExistsException,
    UpdateVendorDenied,
    UpdateVendorStatusDenied,
)

from .product import ProductOwnerRequired, AcceptedVendorRequired
from .cart import CartItemOwnerException, CartItemQuantityException, CartItemNotFound

user_exceptions = [
    "UserAlreadyExistError",
    "UserPendingVerificationError",
    "UserNotFoundError",
    "InvalidVerificationCodeError",
    "InvalidCredentialsError",
]

vendor_exceptions = [
    "PendingVendorExistsException",
    "RejectedVendorExistsException",
    "AcceptedVendorExistsException",
    "UpdateVendorDenied",
    "UpdateVendorStatusDenied",
]

product_exceptions = ["ProductOwnerRequired", "AcceptedVendorRequired"]

cart_exceptions = [
    "CartItemOwnerException",
    "CartItemQuantityException",
    "CartItemNotFound",
]


__all__ = user_exceptions + vendor_exceptions + product_exceptions + cart_exceptions
