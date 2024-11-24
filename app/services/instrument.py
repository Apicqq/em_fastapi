from typing import Optional
from http import HTTPStatus

from fastapi.exceptions import HTTPException
from app.services.base import BaseService
from app.units_of_work.base import atomic


class InstrumentService(BaseService):
    base_repository: str = "instruments"

    @atomic
    async def get_last_trading_days(self, num_dates: int):
        """Get last trading days."""
        self._validate_num_dates(num_dates)
        return await self.uow.instruments.get_last_trading_dates(num_dates)



    @atomic
    async def get_dynamics(self, **kwargs):
        """Get dynamics."""
        return await self.uow.instruments.get_dynamics(**kwargs)


    @atomic
    async def get_trading_results(self):
        """Get trading results."""
        return await self.uow.instruments.get_trading_results()


    @classmethod
    def _validate_num_dates(cls, num_dates: Optional[int]):
        if not isinstance(num_dates, int) or num_dates <= 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Number of dates must be a positive integer",
            )