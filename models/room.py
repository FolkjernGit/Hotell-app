from sqlalchemy.orm import Mapped
from models.base import Base
from shortcuts import pkey, s_int

class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[pkey]
    room_number: Mapped[s_int]
    room_count: Mapped[s_int] 
    
    def __repr__(self) -> str:
        return super().__repr__()