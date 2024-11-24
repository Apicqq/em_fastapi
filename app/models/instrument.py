from datetime import datetime

from sqlalchemy import String, Float, Date, DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class InstrumentDB(Base):
    """Class which represents Instrument model in SQLAlchemy database."""

    exchange_product_id: Mapped[str] = mapped_column(String(30))
    exchange_product_name: Mapped[str] = mapped_column(String(300))
    oil_id: Mapped[str] = mapped_column(String(30))
    delivery_basis_id: Mapped[str] = mapped_column(String(30))
    delivery_basis_name: Mapped[str] = mapped_column(String(50))
    delivery_type_id: Mapped[str] = mapped_column(String(30))
    volume: Mapped[float] = mapped_column(Float)
    total: Mapped[float] = mapped_column(Float)
    count: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(Date, default=datetime.now().date)
    created_on: Mapped[datetime] = mapped_column(DateTime)
    updated_on: Mapped[datetime] = mapped_column(DateTime)
