from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Awaitable, Callable, Optional
from types import TracebackType

from app.database.db import AsyncSessionLocal
from app.models.instrument import InstrumentDB
from app.repositories.instrument import InstrumentRepository


def atomic(
    func: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """Decorate function with transaction mode."""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper


class AbstractUnitOfWork(ABC):
    """
    Abstract base class for Units of Work.

    Provides a context manager interface for database transactions.

    Implementations must provide initialization,
     async context management, and transaction control methods.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initialize the class."""
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> None:
        """Initialize context manager."""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Close the context manager."""
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        """Commit changes to the database."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Cancel pending changes."""
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions."""

    def __init__(self) -> None:
        """Initialize the class, adding session_factory."""
        self.session_factory = AsyncSessionLocal

    async def __aenter__(self) -> None:
        """
        Initialize the context manager.

        Initialization includes creating a session via session factory,
        and also injecting model-specific repository.
        """
        self.session = self.session_factory()
        self.instruments = InstrumentRepository(self.session, InstrumentDB)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Close context manager.

        If there were no exceptions, commit transaction, rollback it otherwise.

        Close the session afterward.
        """
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        """Commit changes to the database."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback pending changes."""
        await self.session.rollback()
