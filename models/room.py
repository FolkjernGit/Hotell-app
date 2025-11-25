from sqlalchemy.orm import Mapped
from models.base import Base
from shortcuts import pkey, s_int
from typing import List

class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[pkey]
    room_number: Mapped[s_int]
    room_count: Mapped[s_int] 
    
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