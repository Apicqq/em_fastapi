from datetime import date
from typing import Any, Sequence

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import select, distinct, Result, between, Select

from app.models.instrument import InstrumentDB
from app.repositories.base import SqlAlchemyRepository


class InstrumentRepository(SqlAlchemyRepository):

    async def get_last_trading_days(self, num_days: int) -> Sequence[date]:
        """Список дат последних торговых дней"""
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
        """Список торгов за заданный период"""
        query: Select = (
            select(self.model)
            .filter(
                between(self.model.date, start_date, end_date),
            )
            .filter_by(**kwargs)
        )
        return await paginate(self.session, query)

    async def get_trading_results(self, **kwargs: Any) -> Page[InstrumentDB]:
        """Список последних торгов"""
        return await paginate(
            self.session,
            select(self.model).filter_by(**kwargs),
        )
