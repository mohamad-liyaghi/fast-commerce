from src.core.database import Base


class BaseUpdateController:
    """
    Base class for handling update operations in db controller
    """

    async def update(self, instance: Base, **data) -> Base:
        """
        Update an instance of a model.
        Takes instance as first argument and data keyword arguments.
        """
        updated_object = await self.repository.update(instance, **data)
        return updated_object
