from src.core.database import Base


class BaseDeleteController:
    """
    Base class for handling delete operations in db controller
    """

    async def delete(self, instance: Base, **kwargs) -> None:
        """
        Delete an instance of a model.
        """
        await self.repository.delete(instance, **kwargs)
