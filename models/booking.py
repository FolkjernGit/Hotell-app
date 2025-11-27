from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timedelta
from typing import List
from shortcuts import s_int

from models.base import Base
from models.mixin import TimestampMixin
from shortcuts import pkey


class Booking(TimestampMixin,Base):
    __tablename__ = "bookings"
    id: Mapped[pkey]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    book_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    booked_duration: Mapped[s_int]
    
    @staticmethod
    def show_available_dates(session):
        booked_dates: List[datetime]
        
        for booking in session.query(Booking).all():
            for i in range(booking.booked_duration): 
                booked_dates += (booking.book_date + timedelta(days=i))
            
        return booked_dates