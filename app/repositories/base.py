from abc import ABC, abstractmethod
from typing import Any, Sequence, TypeVar, TYPE_CHECKING, Union, Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

if TYPE_CHECKING:
    from sqlalchemy import Insert, Select, Update, Delete
    from sqlalchemy.engine import Result

Model = TypeVar("Model", bound=Base)


class AbstractRepository(ABC):
    """
    Abstract Repository class.

    Implements all the CRUD operations for working with any database.
    """

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(
            self,
            *args: Any,
            **kwargs: Any
    ) -> Union[int, str]:
        raise NotImplementedError

    async def add_one_and_get_obj(
            self,
            *args: Any,
            **kwargs: Any
    ) -> type[Model]:
        raise NotImplementedError

    async def get_by_query_one_or_none(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Optional[type[Model]]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all(
            self,
            *args: Any,
            **kwargs: Any
    ) -> Optional[Sequence[Model]]:
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(
            self,
            *args: Any,
            **kwargs: Any
    ) -> Optional[type[Model]]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_query(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """
    Basic repository class.

    Implements all CRUD methods with base table using SQLAlchemy.

    params:
        - model: SQLAlchemy child DeclarativeBase class
    """

    def __init__(
            self,
            session: AsyncSession,
            model: type[Model]
    ) -> None:
        self.session = session
        self.model = model

    async def add_one(self, *args, **kwargs: Any) -> None:
        query: Insert = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_id(self, *args, **kwargs: Any) -> int | str:
        query: Insert = insert(self.model).values(**kwargs).returning(
            self.model.id)
        obj_id: Result = await self.session.execute(query)
        return obj_id.scalar_one()

    async def add_one_and_get_obj(self, **kwargs: Any) -> Model:
        query: Insert = insert(self.model).values(**kwargs).returning(
            self.model)
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def get_by_query_one_or_none(self, **kwargs: Any) -> Model | None:
        query: Select = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all(
            self,
            *args,
            **kwargs: Any
    ) -> Optional[Sequence[Model]]:
        query: Select = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def update_one_by_id(
            self,
            obj_id: int | str,
            **kwargs: Any,
    ) -> Optional[Model]:
        query: Update = (
            update(self.model)
            .filter(
                self.model.id == obj_id,
            )
            .values(**kwargs)
            .returning(self.model)
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one_or_none()

    async def delete_by_query(self, **kwargs: Any) -> None:
        query: Delete = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)

    async def delete_all(self) -> None:
        query: Delete = delete(self.model)
        await self.session.execute(query)
