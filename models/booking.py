import calendar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timedelta
from typing import List
from models.guest import Guest
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
    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    book_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    booked_duration: Mapped[s_int]
    
    def __repr__(self):
        return f"Booked date:{self.book_date} Duration{self.booked_duration} RoomID:{self.room_id}"
    
    @staticmethod
    def create_booking(session,
                       room_number: int,
                       email: str,
                       book_day: int,
                       booked_duration: int,
                       month: int
                       ) -> None:
        '''Metod för skapa bokningar,
            returnerar ett objekt från Booking klassen
        '''
        room_id = session.query(Room.id)\
            .where(Room.room_number==room_number)\
            .scalar()
        guest_id = session.query(Guest.id)\
            .where(Guest.email==email)\
            .scalar()
        book_date = datetime(datetime.now().year,month,book_day)
        
        new_booking = Booking(room_id=room_id,
                            guest_id=guest_id,
                            book_date=book_date,
                            booked_duration=booked_duration
                            )
        
        session.add(new_booking)
        session.commit()
    
    @staticmethod # TODO fixa så inte dagar går över månadens dagar
    def check_rooms( session, month : int, room_id) -> List[datetime]:
        '''Tar in ett rum och månad och returnar en lista med 
            lediga datum för den månaden i det rummet
        '''
        year: DateTime[year] = datetime.now().year
        free_dates: List[datetime] = []

        _, num_days = calendar.monthrange(year, month) # Jag använder _ för att jag bara bryr mig om antal dagar
        
        # hämtar all boknings datum och tid för det valda rummet som en tuple
        book = session.query(Booking.book_date,Booking.booked_duration)\
            .where(Booking.room_id==room_id)\
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
        return free_dates, booked_dates
    
    @staticmethod
    def create_seeding(session):
        bookings: List[Booking] = []

        room_ids = [r[0] for r in session.query(Room.id).all()]
        guest_ids = [r[0] for r in session.query(Guest.id).all()]
        year = 2025

        BOOKINGS_PER_MONTH = 1

        for month in range(1, 13):
            _, num_days = calendar.monthrange(year, month)

            for _ in range(BOOKINGS_PER_MONTH):
                room_id = choice(room_ids)
                guest_id = choice(guest_ids)
                duration = randint(1, 5)  # max 5 dagar

                # se till att bokningen ryms i månaden
                start_day = randint(1, num_days - duration + 1)

                start_date = datetime(year, month, start_day)

                booking = Booking(
                    room_id=room_id,
                    guest_id=guest_id,
                    book_date=start_date,
                    booked_duration=duration
                )

                bookings.append(booking)

        return bookings

