from datetime import date
from typing import Sequence

from sqlalchemy import select, distinct, Result, between

from app.models.instrument import InstrumentDB
from app.repositories.base import SqlAlchemyRepository
from app.schemas.product import InstrumentDateResponse


class InstrumentRepository(SqlAlchemyRepository):
    model = InstrumentDB

    async def get_last_trading_dates(self, num_days: int) -> Sequence[model]:
        """Список дат последних торговых дней"""
        query = select(distinct(self.model.date)).order_by(
            self.model.date.desc()
        ).limit(num_days)
        result: Result = await self.session.execute(query)
        return [InstrumentDateResponse(
            date=_date
        ) for _date in result.scalars().all()]

    async def get_dynamics(self, start_date: date, end_date: date, **kwargs):
        """Список торгов за заданный период"""
        query = select(self.model).filter_by(**kwargs).filter(
            between(self.model.date, start_date, end_date)
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def get_trading_results(self, oil_id: str, delivery_type_id: str,
                                  delivery_basis_id: str):
        """Список последних торгов"""
        query = select(self.model).filter(
            self.model.oil_id == oil_id,
            self.model.delivery_type_id == delivery_type_id,
            self.model.delivery_basis_id == delivery_basis_id
        ).order_by(self.model.date.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
