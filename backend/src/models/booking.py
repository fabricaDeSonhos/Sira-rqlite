import datetime 
from typing import Optional, List
from colour import Color
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ColorType
from sqlalchemy import Date, Time, DateTime, ForeignKey, JSON

from database.base import Base

class CategoryTable(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    color: Mapped[Color] = mapped_column(ColorType)

class BookingTable(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column() # Temporário: será chave estrangeira
    artifact: Mapped[str] = mapped_column()
    date: Mapped[datetime.date] = mapped_column(Date)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    purpose: Mapped[str] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    batch_id: Mapped[Optional[str]] = mapped_column() # Temporário: será chave estrangeira
    observations: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    canceler_user: Mapped[Optional[str]] = mapped_column() # Temporário: será chave estrangeira
    observers: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list) # Temporário: será lista de chaves estrangeiras