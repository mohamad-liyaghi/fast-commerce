from fastapi import Depends, status
from fastapi.routing import APIRouter
from typing import List, Optional
from uuid import UUID
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired, VendorRequired
from src.app.controllers import ProductController
from src.app.schemas.in_ import ProductCreateIn, ProductUpdateIn
from src.app.schemas.out import (
    ProductCreateOut,
    ProductListOut,
    ProductRetrieveOut,
    ProductUpdateOut,
)
from src.app.models import User, Vendor


router = APIRouter(
    tags=["Products"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    request: ProductCreateIn,
    auth: User = Depends(AuthenticationRequired()),
    vendor: Vendor = Depends(VendorRequired()),
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> ProductCreateOut:
    """Create a new product."""
    return await product_controller.create(
        request_user=auth, request_vendor=vendor, data=request.model_dump()
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_product_list(
    title: Optional[str] = None,
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> Optional[List[ProductListOut]]:
    """Get a list of products."""

    return await product_controller.retrieve_or_search(
        many=True, order_by=["created_at"], descending=True, limit=40, title=title
    )


@router.get("/{product_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_product(
    product_uuid: UUID,
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> ProductRetrieveOut:
    """Retrieve a product."""
    return await product_controller.get_by_uuid(
        uuid=product_uuid, join_fields=["vendor", "user"]
    )


@router.put("/{product_uuid}", status_code=status.HTTP_200_OK)
async def update_product(
    product_uuid: UUID,
    request: ProductUpdateIn,
    current_user: User = Depends(AuthenticationRequired()),
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> ProductUpdateOut:
    """Update a product."""
    return await product_controller.update_product(
        uuid=product_uuid,
        request_user=current_user,
        data=request.model_dump(),
    )


@router.delete("/{product_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_uuid: UUID,
    current_user: User = Depends(AuthenticationRequired()),
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> None:
    """Delete a product."""
    await product_controller.delete_product(
        uuid=product_uuid, request_user=current_user
    )
