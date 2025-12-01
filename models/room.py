from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from models.base import Base
from shortcuts import pkey, s_int, dec
from typing import List


class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[pkey]
    room_number: Mapped[s_int]
    room_count: Mapped[s_int] 
    #booked: Mapped[bool] = mapped_column(Boolean)
    price_per_night: Mapped[dec]
    
    
    def book_room(self):
        pass
    
    @staticmethod
    def create_seeding() -> List["Room"]:
    
        rooms: List[Room] = [] 
        
        new_room1 = Room(room_number=1,room_count=1,price_per_night=300)
        new_room2 = Room(room_number=2,room_count=1,price_per_night=300)
        new_room3 = Room(room_number=3,room_count=2,price_per_night=500)
        new_room4 = Room(room_number=4,room_count=2,price_per_night=500)
        
        rooms.append(new_room1)
        rooms.append(new_room2)
        rooms.append(new_room3)
        rooms.append(new_room4)
        
        return rooms

    @staticmethod
    def get_rooms(session):
        rooms = session.query(Room.room_number,Room.room_count,Room.price_per_night,Room.id).all()
        return rooms