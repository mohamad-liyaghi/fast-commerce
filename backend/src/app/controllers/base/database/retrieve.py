from fastapi import HTTPException, status
from typing import List, Optional, Union
from uuid import UUID
from src.core.database import Base


class BaseRetrieveController:
    """
    Base class for handling retrieve operations in db controller
    """

    async def retrieve(
        self,
        join_fields: Optional[List[str]] = None,
        order_by: Optional[list] = None,
        descending: bool = False,
        many: bool = False,
        limit: int = 100,
        skip: int = 0,
        contains: bool = False,
        _in: bool = False,
        **kwargs
    ) -> Union[List[Base], Base, None]:
        """
        Retrieve an instance of model.
        Params:
            join_fields: a list of fields to join the object with.
            order_by: a list of fields to order the results by.
            descending: a boolean indicating the order of the results should be descending.
            many: return query results as a list if True, otherwise return a single object.
            limit: the maximum number of results to return.
            skip: the number of results to skip.
            contains: used for filtering, indicate that the query should be
                      exact or partial match.
            _in: used to filter results by a list of values.

        """
        result = await self.repository.retrieve(
            join_fields=join_fields,
            limit=limit,
            skip=skip,
            many=many,
            descending=descending,
            order_by=order_by,
            contains=contains,
            _in=_in,
            **kwargs
        )
        return result if result else None

    async def get_by_id(
        self, _id: int, not_found_message: str = "item not found", **kwargs
    ) -> Base:
        """
        Retrieve an instance by id
        If not found, raise an HTTPException with status code 404
        """
        result = await self.retrieve(id=_id, **kwargs)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=not_found_message
            )
        return result

    async def get_by_uuid(
        self, uuid: UUID, not_found_message: str = "item not found", **kwargs
    ) -> Base:
        """
        Get an instance by uuid
        Raise an HTTPException with status code 404 if not found
        """
        result = await self.retrieve(uuid=uuid, **kwargs)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=not_found_message
            )
        return result
