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
    VendorRequiredException,
)

from .product import ProductOwnerRequired, AcceptedVendorRequired, ProductNotFound
from .cart import (
    CartItemOwnerException,
    CartItemQuantityException,
    CartItemNotFound,
    CartEmptyException,
)
from .order import OrderAlreadyPaid
from .admin import AdminRequiredException
from .order_item import InappropriateOrderStatus

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
    "VendorRequiredException",
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

order_exceptions = ["OrderAlreadyPaid"]
admin_exceptions = ["AdminRequiredException"]
order_item_exceptions = ["InappropriateOrderStatus"]

__all__ = (
    user_exceptions
    + vendor_exceptions
    + product_exceptions
    + cart_exceptions
    + order_exceptions
    + admin_exceptions
    + order_item_exceptions
)
