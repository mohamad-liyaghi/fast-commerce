from .core import AlreadyExistError


class PendingVendorExistsException(AlreadyExistError):
    def __init__(self, message="Pending vendor already exists"):
        super().__init__(message)


class RejectedVendorExistsException(Exception):
    def __init__(self, message="Rejected vendor already exists"):
        super().__init__(message)


class AcceptedVendorExistsException(Exception):
    def __init__(self, message="Accepted vendor already exists"):
        super().__init__(message)


class UpdateVendorStatusDenied(Exception):
    def __init__(self, message="Only Admins can update vendor status."):
        super().__init__(message)


class UpdateVendorDenied(Exception):
    def __init__(self, message="You cannot update others vendor record."):
        super().__init__(message)


class VendorRequiredException(Exception):
    def __init__(self, message="User is not the objects vendor."):
        super().__init__(message)
