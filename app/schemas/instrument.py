from datetime import datetime, date
from typing import Annotated, Self, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveFloat,
    model_validator,
)


class InstrumentOut(BaseModel):
    """
    Base Pydantic schema for Instrument model.

    Represents all existing fields of the model.
    """

    id: int
    exchange_product_id: Annotated[str, Field(..., max_length=11)]
    exchange_product_name: str
    oil_id: Annotated[str, Field(..., max_length=4)]
    delivery_basis_id: Annotated[str, Field(..., max_length=3)]
    delivery_basis_name: str
    delivery_type_id: Annotated[str, Field(..., max_length=1)]
    volume: PositiveFloat
    total: PositiveFloat
    count: PositiveFloat
    date: date
    created_on: datetime
    updated_on: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class InstrumentDateResponse(BaseModel):
    """Schema for representing date of a trading day."""

    date: date


class InstrumentFilters(BaseModel):
    """Schema for representing filters applied to Instruments model."""

    oil_id: Annotated[str, Field(None, max_length=4)]
    delivery_type_id: Annotated[str, Field(None, max_length=1)]
    delivery_basis_id: Annotated[str, Field(None, max_length=3)]


class InstrumentWithDateFilters(InstrumentFilters):
    """
    Schema for representing filters applied to Instruments model.

    Also includes start_date and end_date fields.
    """

    @model_validator(mode="after")
    def validate_timedelta(self) -> Self:
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError(
                    "start_date must be less or equal than end_date"
                )
        return self

    start_date: date
    end_date: date
