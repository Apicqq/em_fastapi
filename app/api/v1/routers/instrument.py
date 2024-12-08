from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from fastapi_pagination import Page

from app.schemas.instrument import (
    InstrumentOut,
    InstrumentDateResponse,
    InstrumentFilters,
    InstrumentWithDateFilters,
)
from app.services.instrument import InstrumentService

router = APIRouter(prefix="/instrument")


@router.get(
    "/get_last_trading_days",
    response_model=list[InstrumentDateResponse],
)
# @cache()
async def get_last_trading_days(
    num_dates: int,
    service: InstrumentService = Depends(InstrumentService),
) -> list[InstrumentDateResponse]:
    return await service.get_last_trading_days(num_dates)


@router.get(
    "/get_dynamics",
    response_model=Page[InstrumentOut],
)
# @cache()
async def get_dynamics(
    filters_query: Annotated[InstrumentWithDateFilters, Query()],
    service: InstrumentService = Depends(InstrumentService),
) -> Page[InstrumentOut]:
    return await service.get_dynamics(
        **filters_query.model_dump(
            exclude_unset=True,
        ),
    )


@router.get(
    "/get_trading_results",
    response_model=Page[InstrumentOut],
)
# @cache()
async def get_trading_results(
    filters_query: Annotated[InstrumentFilters, Query()],
    service: InstrumentService = Depends(InstrumentService),
) -> Page[InstrumentOut]:
    return await service.get_trading_results(
        **filters_query.model_dump(exclude_unset=True),
    )
