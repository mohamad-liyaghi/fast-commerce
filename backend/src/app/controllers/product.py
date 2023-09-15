from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID
from src.app.models import User, Vendor, Product
from src.app.controllers import BaseController
from src.app.repositories import ProductRepository
from src.core.exceptions import ProductOwnerRequired, AcceptedVendorRequired


class ProductController(BaseController):
    """
    Controller for managing product related requests.
    """

    def __init__(self, repository: ProductRepository):
        self.repository = repository
        super().__init__(repository)

    async def create(
        self, request_user: User, request_vendor: Vendor, data: dict
    ) -> Product:
        try:
            return await super().create(
                request_user=request_user, request_vendor=request_vendor, **data
            )
        except AcceptedVendorRequired:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not an accepted vendor.",
            )

    async def update_product(
        self, uuid: UUID, request_user: User, data: dict
    ) -> Product:
        product = await self.get_by_uuid(uuid=uuid)

        try:
            return await self.repository.update_product(
                instance=product, request_user=request_user, data=data
            )

        except ProductOwnerRequired:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this product.",
            )

    async def delete_product(self, uuid: UUID, request_user: User) -> None:
        product = await self.get_by_uuid(uuid=uuid)

        try:
            return await self.repository.delete_product(
                instance=product, request_user=request_user
            )

        except ProductOwnerRequired:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this product.",
            )

    async def retrieve_or_search(
        self, title: Optional[str] = None, many: bool = False, **kwargs
    ):
        """
        Retrieve a list of products or search for a product by title.
        If title is not None, set as kwargs to filter it.
        """

        if title:
            kwargs["title"] = title

        return await super().retrieve(many=many, contains=True, **kwargs)
