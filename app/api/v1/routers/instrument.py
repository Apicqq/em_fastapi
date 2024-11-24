from typing import Optional, Annotated
from datetime import date

from fastapi import APIRouter, Depends, Body, Query
from fastapi_pagination import Page

from app.schemas.product import (
    InstrumentOut,
    InstrumentDateResponse,
    InstrumentFilters,
    InstrumentWithDateFilters
)
from app.services.instrument import InstrumentService

router = APIRouter(prefix="/instrument")


@router.get(
    "/",
    response_model=list[InstrumentOut],
)
async def get_all_instruments(
        service: InstrumentService = Depends(InstrumentService)
):
    return await service.get_by_query_all(exchange_product_id="A100NVY060F")


@router.get(
    "/get_last_trading_days",
    response_model=list[InstrumentDateResponse],
)
async def get_last_trading_days(
        num_dates: int,
        service: InstrumentService = Depends(InstrumentService)
) -> list[InstrumentDateResponse]:
    return await service.get_last_trading_days(num_dates)


@router.get("/get_dynamics")
async def get_dynamics(
        filters_query: Annotated[InstrumentWithDateFilters, Query()],
        service: InstrumentService = Depends(InstrumentService)
) -> list[InstrumentOut]:
    return await service.get_dynamics(**filters_query.model_dump(
        exclude_unset=True
    ))


@router.get("/get_trading_results")
async def get_trading_results(
        filters: Annotated[InstrumentFilters, Query()],
        service: InstrumentService = Depends(InstrumentService)
) -> list[InstrumentOut]:
    return await service.get_trading_results(
        **filters.model_dump(exclude_unset=True)
    )
