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

from .product import ProductOwnerRequired, AcceptedVendorRequired, ProductNotFound
from .cart import (
    CartItemOwnerException,
    CartItemQuantityException,
    CartItemNotFound,
    CartEmptyException,
)

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

product_exceptions = [
    "ProductOwnerRequired",
    "AcceptedVendorRequired",
    "ProductNotFound",
]

cart_exceptions = [
    "CartItemOwnerException",
    "CartItemQuantityException",
    "CartItemNotFound",
    "CartEmptyException",
]


__all__ = user_exceptions + vendor_exceptions + product_exceptions + cart_exceptions
