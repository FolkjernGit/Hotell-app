import calendar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timedelta
from typing import List
from shortcuts import s_int

import calendar
from random import choice, randint
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
    
    def __repr__(self):
        return f"Booked date:{self.book_date} Duration{self.booked_duration} RoomID:{self.room_id}"
    
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
        booked_dates = []

        for b in book:
            start_date = b[0]
            duration = b[1]
            for i in range(duration):
                booked_dates.append(start_date.day + i)
        print(booked_dates)

        for day in range(1, num_days + 1):
            if day in booked_dates:
                free_dates.append(f"{day} Booked")
            else:
                free_dates.append(f"{day} Free to book")
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

        year = 2025


        BOOKINGS_PER_MONTH = 1

        for month in range(1, 13): 
            _, num_days = calendar.monthrange(year, month)

            for _ in range(BOOKINGS_PER_MONTH):
                room_id = choice(room_ids)

                start_day = 1

                duration = 20

                start_date = datetime(year, month, start_day)

                booking = Booking(room_id=room_id,book_date=start_date,booked_duration=duration)

                bookings.append(booking)

        return bookings

        