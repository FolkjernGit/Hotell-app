from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Boolean
from models.guest import Guest
from models.mixin import TimestampMixin
from models.room import Room
from shortcuts import pkey, dec
from datetime import datetime, timedelta

class Invoice(TimestampMixin,Base):
    __tablename__ = "invoices"
    id: Mapped[pkey]
    amount: Mapped[dec]
    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
    paid: Mapped[bool] = mapped_column(Boolean)
    price_per_night: Mapped[dec]
    expired: Mapped[bool] = mapped_column(Boolean)
    
    def pay_invoice(self):
        self.paid = True
        
    def check_if_expired(self):
        if (datetime.now() - self.created_at) > timedelta(days=10):
            self.expired = True
       
       
    @staticmethod
    def get_amount(session, duration, room_number) -> int:
        '''Takes duration and price_per_night and returns product
        '''
        price_per_night = session.query(Room.price_per_night)\
            .where(Room.room_number==room_number)\
            .scalar()
            
        return price_per_night * duration
        
            
    @staticmethod
    def create_invoice(session, email, room_number, amount)  -> None:
        '''Finds guest_id using email and room_id using room_number
        '''
        guest_id = session.query(Guest.id)\
            .where(Guest.email==email)\
            .scalar()
        
        price_per_night = session.query(Room.price_per_night)\
            .where(Room.room_number==room_number)\
            .scalar()
            

        new_invoice = Invoice(
            amount=amount,
            guest_id=guest_id,
            paid=False,
            price_per_night=price_per_night,
            expired=False)

        session.add(new_invoice)
        session.commit()