from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field


class InstrumentFull(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: float
    total: float
    count: float
    date: date
    created_on: datetime
    updated_on: Optional[datetime]


class InstrumentDateResponse(BaseModel):
    date: date


class InstrumentFilters(BaseModel):
    oil_id: Optional[str] = Field(None, max_length=4)
    delivery_type_id: Optional[str] = Field(None, max_length=1)
    delivery_basis_id: Optional[str] = Field(None, max_length=3)


class InstrumentFiltersWithDate(InstrumentFilters):
    start_date: date
    end_date: date