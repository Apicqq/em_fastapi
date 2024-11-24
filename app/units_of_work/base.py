from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Awaitable, Callable, Never, Optional
from types import TracebackType

from app.database.db import AsyncSessionLocal
from app.repositories.instrument import InstrumentRepository


def atomic(
        func: Callable[..., Awaitable[Any]]
) -> Callable[..., Awaitable[Any]]:
    """Decorate function with transaction mode."""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper


class AbstractUnitOfWork(ABC):

    @abstractmethod
    def __init__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> Never:
        raise NotImplementedError



class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions."""

    def __init__(self) -> None:
        self.session_factory = AsyncSessionLocal

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.instruments = InstrumentRepository(self.session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
