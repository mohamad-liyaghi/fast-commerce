from src.core.database import Base


class BaseDeleteRepository:
    """
    This repository is responsible for all the database delete operations
    """

    async def delete(self, instance: Base) -> None:
        """
        Delete an instance of model
        :param instance: instance to delete
        :return: None
        """
        await self.session.delete(instance)
        await self.session.commit()
