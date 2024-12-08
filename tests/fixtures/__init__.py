"""The package contains various data used in tests."""

__all__ = [
    "FakeBaseService",
    "FakeInstrumentService",
    "FakeUnitOfWork",
    "test_cases",
]

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.instrument import InstrumentService
from app.models.instrument import InstrumentDB
from app.repositories.instrument import InstrumentRepository
from app.services.base import BaseService
from app.units_of_work.base import UnitOfWork
from tests.fixtures import test_cases


class FakeUnitOfWork(UnitOfWork):
    """Test class for overriding the standard UnitOfWork.
    Provides isolation using transactions at the level of a single TestCase.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def __aenter__(self) -> None:
        self.instruments = InstrumentRepository(self._session, InstrumentDB)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.flush()


class FakeBaseService(BaseService):
    """..."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)


class FakeInstrumentService(FakeBaseService, InstrumentService):
    """..."""

    base_repository: str = "instruments"
