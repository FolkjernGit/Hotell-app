from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base import Base
from shortcuts import pkey, str_255
from typing import List
from models.mixin import TimestampMixin, SoftDeletionMixin

class Guest(SoftDeletionMixin,TimestampMixin,Base):
    __tablename__ = "guests"
    id: Mapped[pkey]
    first_name: Mapped[str_255]
    last_name: Mapped[str_255]
    email: Mapped[str_255] = mapped_column(unique=True)
    
    @staticmethod
    def add_guest(session, full_name, email):
        first_name, last_name = full_name.split()
        first_name, last_name = first_name.capitalize(), last_name.capitalize()
        new_guest = Guest(first_name=first_name,
                          last_name=last_name,
                          email=email)
        session.add(new_guest)
        session.commit()
    
    # seeding
    @staticmethod
    def create_seeding() -> List["Guest"]:
        
        guests: List[Guest] = []
        
        new_guest1 = Guest(first_name='Linus',last_name='Folkjern',email='folkjern@icloud.com')
        new_guest2 = Guest(first_name='Elin',last_name='Sjöberg',email='elin.sjoberg@example.com')
        new_guest3 = Guest(first_name='Marcus',last_name='Hallgren',email='marcus.hallgren@example.com')
        new_guest4 = Guest(first_name='Tilda',last_name='Bergström',email='tilda.bergstrom@example.com')
        
        guests.append(new_guest1)
        guests.append(new_guest2)
        guests.append(new_guest3)
        guests.append(new_guest4)
        
        return guests
        