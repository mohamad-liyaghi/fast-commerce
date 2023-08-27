from fastapi import Depends, status
from fastapi.routing import APIRouter
from typing import List, Optional
from uuid import UUID
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired, VendorRequired
from src.app.controllers import ProductController
from src.app.schemas.in_ import ProductCreateIn
from src.app.schemas.out import ProductCreateOut, ProductListOut, ProductRetrieveOut


router = APIRouter(
    tags=["Products"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    request: ProductCreateIn,
    auth: AuthenticationRequired = Depends(AuthenticationRequired()),
    vendor: VendorRequired = Depends(VendorRequired()),
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> ProductCreateOut:
    """Create a new product."""
    return await product_controller.create(
        request_user=auth, request_vendor=vendor, data=request.model_dump()
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_product_list(
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> Optional[List[ProductListOut]]:
    """Get a list of products."""
    return await product_controller.list()  # TODO: add order


@router.get("/{product_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_product(
    product_uuid: UUID,
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> ProductRetrieveOut:
    """Retrieve a product."""
    return await product_controller.get_by_uuid(
        uuid=product_uuid, join_fields=["vendor", "user"]
    )
