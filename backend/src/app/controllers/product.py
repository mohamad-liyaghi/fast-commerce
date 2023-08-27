from fastapi import HTTPException, status
from uuid import UUID
from src.app.models import User
from src.app.controllers.base import BaseController


class ProductController(BaseController):
    """
    Controller for managing product related requests.
    """

    async def create(self, request_user, request_vendor, data):
        """
        Create a product.
        """
        data.setdefault("vendor_id", request_vendor.id)
        data.setdefault("user_id", request_user.id)
        return await super().create(**data)

    async def update(self, uuid: UUID, request_user: User, data):
        """
        Update a product.
        """
        product = await self.get_by_uuid(uuid=uuid)
        if product.user_id != request_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this product.",
            )

        return await super().update(product, **data)

    async def delete(self, uuid: UUID, request_user: User):
        """
        Delete a product.
        """
        product = await self.get_by_uuid(uuid=uuid)

        if product.user_id != request_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this product.",
            )

        return await super().delete(product)
