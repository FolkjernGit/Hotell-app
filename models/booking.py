from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from shortcuts import s_int

from models.base import Base
from models.mixin import TimestampMixin
from shortcuts import pkey


class Booking(TimestampMixin,Base):
    __tablename__ = "bookings"
    id: Mapped[pkey]
    guest_ID: Mapped[int] = mapped_column(ForeignKey("guests.id"), primary_key=True)
    room_ID: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    book_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    booked_duration: Mapped[s_int]
    
    