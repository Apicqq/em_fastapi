from collections.abc import Sequence
from typing import Any

from app.units_of_work.base import atomic, UnitOfWork


class BaseService:
    """
    A basic service for performing standard CRUD operations with the base repository.

    params:
        - base_repository: should be string like AbstractUnitOfWork class params
    """

    base_repository: str

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    @atomic
    async def add_one(self, **kwargs: Any) -> None:
        await getattr(self.uow, self.base_repository).add_one(**kwargs)

    @atomic
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str:
        return await getattr(
            self.uow, self.base_repository,
        ).add_one_and_get_id(**kwargs)

    @atomic
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        return await getattr(
            self.uow, self.base_repository,
        ).add_one_and_get_obj(**kwargs)

    @atomic
    async def get_by_query_one_or_none(self, **kwargs: Any) -> Any:
        return await getattr(
            self.uow, self.base_repository,
        ).get_by_query_one_or_none(**kwargs)

    @atomic
    async def get_by_query_all(self, **kwargs: Any) -> Sequence[Any]:
        return await getattr(self.uow, self.base_repository).get_by_query_all(
            **kwargs,
        )

    @atomic
    async def update_one_by_id(self, obj_id: int | str, **kwargs: Any) -> Any:
        return await getattr(self.uow, self.base_repository).update_one_by_id(
            obj_id, **kwargs,
        )

    @atomic
    async def delete_by_query(self, **kwargs: Any) -> None:
        await getattr(self.uow, self.base_repository).delete_by_query(**kwargs)

    @atomic
    async def delete_all(self) -> None:
        await getattr(self.uow, self.base_repository).delete_all()
