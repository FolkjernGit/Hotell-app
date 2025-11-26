from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from models.base import Base
from shortcuts import pkey, s_int
from typing import List
from database.db import My_Session

class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[pkey]
    room_number: Mapped[s_int]
    room_count: Mapped[s_int] 
    booked: Mapped[bool] = mapped_column(Boolean)
    
    @staticmethod
    def show_avaible_rooms(session):
        
        
        available_rooms = (
            session.query(Room)\
            .where(Room.booked==False)\
            .all()
            )
        
        available_room_list = ""
        
        for room in available_rooms:
            available_room_list += f"Room number: {room.room_number} Room count: {room.room_count}\n"
        
        return available_room_list
    
    def book_room(self):
        pass
    
    @staticmethod
    def create_seeding() -> List["Room"]:
    
        rooms: List[Room] = [] 
        
        new_room1 = Room(room_number=1,room_count=1)
        new_room2 = Room(room_number=2,room_count=1)
        new_room3 = Room(room_number=3,room_count=2)
        new_room4 = Room(room_number=4,room_count=2)
        
        rooms.append(new_room1)
        rooms.append(new_room2)
        rooms.append(new_room3)
        rooms.append(new_room4)
        
        return rooms

