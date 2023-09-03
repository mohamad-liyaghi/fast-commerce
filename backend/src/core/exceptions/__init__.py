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


__all__ = user_exceptions + vendor_exceptions
