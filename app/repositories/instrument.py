from datetime import date
from typing import Sequence

from sqlalchemy import select, distinct, Result, between

from app.models.instrument import InstrumentDB
from app.repositories.base import SqlAlchemyRepository
from app.schemas.product import InstrumentDateResponse


class InstrumentRepository(SqlAlchemyRepository):
    model = InstrumentDB

    async def get_last_trading_days(self, num_days: int) -> Sequence[model]:
        """Список дат последних торговых дней"""
        query = select(distinct(self.model.date)).order_by(
            self.model.date.desc()
        ).limit(num_days)
        result: Result = await self.session.execute(query)
        return [
            InstrumentDateResponse(date=_date)
            for _date in result.scalars().all()
        ]

    async def get_dynamics(self, start_date: date, end_date: date, **kwargs):
        """Список торгов за заданный период"""
        query = select(self.model).filter(
            between(self.model.date, start_date, end_date)
        ).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def get_trading_results(self, **kwargs):
        """Список последних торгов"""
        return await self.get_by_query_all(**kwargs)
