from sqlalchemy.orm import Mapped
from base import Base
from shortcuts import pkey, s_int

class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[pkey]
    room_number: Mapped[s_int]
    room_count: Mapped[s_int] 
    
