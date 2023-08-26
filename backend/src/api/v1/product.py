from fastapi import Depends, status
from fastapi.routing import APIRouter
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired, VendorRequired
from src.app.controllers import ProductController
from src.app.schemas.in_ import ProductCreateIn
from src.app.schemas.out import ProductCreateOut


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
    return await product_controller.create(
        request_user=auth, request_vendor=vendor, data=request.model_dump()
    )
