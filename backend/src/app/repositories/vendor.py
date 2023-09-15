from datetime import datetime, timedelta
from src.app.repositories.base import BaseRepository
from src.app.models import User, Vendor
from src.app.enums import VendorStatusEnum
from src.core.exceptions import (
    AcceptedVendorExistsException,
    PendingVendorExistsException,
    RejectedVendorExistsException,
    UpdateVendorStatusDenied,
    VendorInformationUpdateDenied,
)


class VendorRepository(BaseRepository):
    """
    Vendor Repository is responsible db/cache operations of vendor model.
    """

    async def create(self, request_user: User, **vendor_data) -> Vendor:
        existing_vendor = await self.retrieve(owner_id=request_user.id, descending=True)

        if existing_vendor:
            if existing_vendor.status == VendorStatusEnum.PENDING:
                raise PendingVendorExistsException()

            elif existing_vendor.status == VendorStatusEnum.ACCEPTED:
                raise AcceptedVendorExistsException()

            elif (
                existing_vendor.status == VendorStatusEnum.REJECTED
                and existing_vendor.reviewed_at > datetime.utcnow() - timedelta(days=10)
            ):
                raise RejectedVendorExistsException()

        vendor_data["owner_id"] = request_user.id
        return await super().create(**vendor_data)

    async def update_vendor(
        self, instance: Vendor, request_user: User, **data
    ) -> Vendor:
        # If status is in data, that means we are updating the status of the vendor.
        status_in_data = data.get("status")

        if status_in_data and not request_user.is_admin:
            raise UpdateVendorStatusDenied

        # If status is not in data, that means we are updating the information of the vendor.
        if not status_in_data and not request_user.id == instance.owner_id:
            raise VendorInformationUpdateDenied

        return await super().update(instance=instance, **data)
