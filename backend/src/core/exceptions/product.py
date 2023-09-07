class ProductOwnerRequired(Exception):
    def __init__(self, message="You cannot update others product record."):
        super().__init__(message)


class AcceptedVendorRequired(Exception):
    def __init__(self, message="You cannot create product without accepted vendor."):
        super().__init__(message)


class ProductNotFound(Exception):
    def __init__(self, message="No product were found."):
        super().__init__(message)
