import calendar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timedelta
from typing import List
from shortcuts import s_int

from random import choice
from models.room import Room
from models.base import Base
from models.mixin import TimestampMixin
from shortcuts import pkey


class Booking(TimestampMixin,Base):
    __tablename__ = "bookings"
    id: Mapped[pkey]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    book_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    booked_duration: Mapped[s_int]
    
    @staticmethod # TODO fixa så inte dagar går över månadens dagar
    def check_rooms( session, month : int, roomID) -> List[datetime]:
        '''Tar in ett rum och månad och returnar en lista med 
            lediga datum för den månaden i det rummet
        '''
        year: DateTime[year] = datetime.now().year
        free_dates: List[datetime] = []

        _, num_days = calendar.monthrange(year, month) # Jag använder _ för att jag bara bryr mig om antal dagar
        
        # hämtar all boknings datum och tid för det valda rummet som en tuple
        book = session.query(Booking.book_date,Booking.booked_duration)\
            .where(Booking.room_id==roomID)\
            .all()
        
        # [(datetime(2025, 8, 20, 0, 0), 3), (datetime(2025, 8, 25, 0, 0), 2)]
        booked_days = []
        
        # loopar igenom book och lägger till bokade datum i en lista
        for b in book:
            for i in range(b[1]):
                booked_days.append((b[0].day)+i)
            
        # loopar i så många dagar det är på månaden som är vald
        # och lägger till lediga datum i en lista
        for day in range(1, num_days + 1):
            if day not in booked_days:
                free_dates.append(datetime(year,month,day))
            
        return free_dates
    
    # @staticmethod
    # def show_available_dates(session):
    #     booked_dates: List[datetime] = []
        
    #     for booking in session.query(Booking)\
    #         .all():
    #         for i in range(booking.booked_duration): 
    #             booked_dates.append(booking.book_date + timedelta(days=i))
    #             booked_dates.append()
                
    #     return booked_dates
    
    @staticmethod
    def create_seeding(session):
        
        bookings: List[Booking] = []
        room_ids = [r[0] for r in session.query(Room.id).all()]
        
        new_booking1 = Booking(room_id=choice(room_ids),book_date=datetime(2025,10,10),booked_duration=5)
        new_booking2 = Booking(room_id=choice(room_ids),book_date=datetime(2025,8,20),booked_duration=3)
        
        bookings.append(new_booking1)
        bookings.append(new_booking2)
        
        return bookings

        