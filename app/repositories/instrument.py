from datetime import date
from typing import Any, Sequence

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import select, distinct, Result, between, Select

from app.models.instrument import InstrumentDB
from app.repositories.base import SqlAlchemyRepository


class InstrumentRepository(SqlAlchemyRepository):
    """
    Repository class for Instrument model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def get_last_trading_days(self, num_days: int) -> Sequence[date]:
        """Get sequence of last trading days."""
        query: Select = (
            select(distinct(self.model.date))
            .order_by(
                self.model.date.desc(),
            )
            .limit(num_days)
        )
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def get_dynamics(
        self,
        start_date: date,
        end_date: date,
        **kwargs: Any,
    ) -> Page[InstrumentDB]:
        """Get trading dynamics for set period."""
        query: Select = (
            select(self.model)
            .filter(
                between(self.model.date, start_date, end_date),
            )
            .filter_by(**kwargs)
        )
        return await paginate(self.session, query)

    async def get_trading_results(self, **kwargs: Any) -> Page[InstrumentDB]:
        """Get sequence of trading results, matched by filters."""
        return await paginate(
            self.session,
            select(self.model).filter_by(**kwargs),
        )
