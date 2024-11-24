from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InstrumentOut(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)


class InstrumentDateResponse(BaseModel):
    date: date


class InstrumentFilters(BaseModel):
    oil_id: Optional[str] = Field(None)
    delivery_type_id: Optional[str] = Field(None)
    delivery_basis_id: Optional[str] = Field(None)

class InstrumentWithDateFilters(InstrumentFilters):
    start_date: Optional[date]
    end_date: Optional[date]
