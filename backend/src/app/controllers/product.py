from fastapi import HTTPException, status
from typing import Optional
from src.app.models import User, Vendor, Product
from src.app.controllers import BaseController
from src.core.exceptions import ProductOwnerRequired, AcceptedVendorRequired
from src.core.sql.types import UUIDType


class ProductController(BaseController):
    """
    Controller for managing product related requests.
    """

    async def create(
        self, request_user: User, request_vendor: Vendor, data: dict
    ) -> Product:
        """
        Create a product.
        """
        try:
            return await super().create(
                request_user=request_user, request_vendor=request_vendor, **data
            )
        except AcceptedVendorRequired:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not an accepted vendor.",
            )

    async def update(self, uuid: UUIDType, request_user: User, data: dict) -> Product:
        """
        Update a product.
        """
        product = await self.get_by_uuid(uuid=uuid)
        try:
            return await super().update(
                instance=product, request_user=request_user, data=data
            )
        except ProductOwnerRequired:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this product.",
            )

    async def delete(self, uuid: UUIDType, request_user: User) -> None:
        """
        Delete a product.
        """
        product = await self.get_by_uuid(uuid=uuid)

        try:
            return await super().delete(instance=product, request_user=request_user)

        except ProductOwnerRequired:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this product.",
            )

    async def retrieve_or_search(
        self, title: Optional[str] = None, many: bool = False, **kwargs
    ):
        """
        Retrieve or search for a product.
        If title is not None, set as kwargs to filter it.
        """

        if title:
            kwargs["title"] = title

        return await super().retrieve(many=many, contains=True, **kwargs)
