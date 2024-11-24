from fastapi import APIRouter, Depends

from app.schemas.product import InstrumentFull, InstrumentDateResponse, \
    InstrumentFilters
from app.services.instrument import InstrumentService

router = APIRouter(prefix="/instrument")


@router.get(
    "/",
    response_model=list[InstrumentFull],
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
    dates = await service.get_last_trading_days(num_dates)
    return [InstrumentDateResponse(date=date) for date in dates]


@router.get("/get_dynamics")
async def get_dynamics(
        filters: InstrumentFilters,
        service: InstrumentService = Depends(InstrumentService)
):
    return await service.get_dynamics(**filters.model_dump(exclude_unset=True))


@router.get("/get_trading_results")
async def get_trading_results():
    pass
