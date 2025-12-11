import calendar
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, String, func
from datetime import datetime, timedelta
from typing import List
from models.guest import Guest
from shortcuts import s_int

import calendar
from models.room import Room
from models.base import Base
from models.mixin import TimestampMixin



class Booking(TimestampMixin,Base):
    __tablename__ = "bookings"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex)

    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    book_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    booked_duration: Mapped[s_int]
    people: Mapped[s_int]
    
    def __repr__(self):
        return f"Booked date:{self.book_date} Duration{self.booked_duration} RoomID:{self.room_id}"
    
    @staticmethod # TODO kolla om gäst är raderad
    def create_booking(session,
                       room_number: int,
                       email: str,
                       book_day: int,
                       booked_duration: int,
                       month: int,
                       people: int
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
                            booked_duration=booked_duration,
                            people=people
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

        _, num_days = calendar.monthrange(year, month)
        
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


        for day in range(1, num_days + 1):
            if day in booked_dates:
                free_dates.append(f"{day} Booked")
            else:
                free_dates.append(f"{day} Free to book")
        return free_dates, booked_dates
    


