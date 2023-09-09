from src.core.database import Base


class BaseUpdateRepository:
    """
    This class is used to update an instance of model
    """

    async def update(self, instance: Base, **data) -> Base:
        """
        Update an instance of model
        :param instance: instance to update
        :param data: data to update
        :return: updated instance
        """
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
