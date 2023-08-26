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
