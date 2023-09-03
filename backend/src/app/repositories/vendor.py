from datetime import datetime, timedelta
from src.app.repositories.base import BaseRepository
from src.app.models import User, VendorStatus, Vendor
from src.core.exceptions import (
    AcceptedVendorExistsException,
    PendingVendorExistsException,
    RejectedVendorExistsException,
    UpdateVendorStatusDenied,
    UpdateVendorDenied,
)


class VendorRepository(BaseRepository):
    """
    Vendor Repository is responsible db/cache operations of vendor model.
    """

    async def create(self, request_user: User, **vendor_data) -> Vendor:
        existing_vendor = await self.retrieve(owner_id=request_user.id, descending=True)

        if existing_vendor:
            if existing_vendor.status == VendorStatus.PENDING:
                raise PendingVendorExistsException()
            elif existing_vendor.status == VendorStatus.ACCEPTED:
                raise AcceptedVendorExistsException()
            elif (
                existing_vendor.status == VendorStatus.REJECTED
                and existing_vendor.reviewed_at > datetime.utcnow() - timedelta(days=10)
            ):
                raise RejectedVendorExistsException()

        vendor_data["owner_id"] = request_user.id
        return await super().create(**vendor_data)

    async def update(self, instance: Vendor, request_user: User, **data) -> Vendor:
        # If status is in data it means user is trying to update vendor status.
        status_in_data = data.get("status")

        if status_in_data and not request_user.is_admin:
            raise UpdateVendorStatusDenied

        if not status_in_data and not request_user.id == instance.owner_id:
            raise UpdateVendorDenied

        return await super().update(instance=instance, **data)
