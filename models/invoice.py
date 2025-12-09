from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Boolean
from models.booking import Booking
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
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    paid: Mapped[bool] = mapped_column(Boolean)
    price_per_night: Mapped[dec]
    expired: Mapped[bool] = mapped_column(Boolean)
    
    def pay_invoice(self):
        self.paid = True
        
    def check_if_expired(self):
        if (datetime.now() - self.created_at) > timedelta(days=10):
            self.expired = True
       
    @staticmethod
    def get_invoice_object(session,email):
        invoice = session.query(Invoice)\
            .join(Guest, Invoice.guest_id == Guest.id)\
            .where(Guest.email == email)\
            .where(Invoice.paid == False)\
            .where(Invoice.expired == False)\
            .all()
        return invoice   
    
    @staticmethod
    def get_amount(session, duration, room_number) -> int:
        '''Takes duration and price_per_night and returns product
        '''
        price_per_night = session.query(Room.price_per_night)\
            .where(Room.room_number==room_number)\
            .scalar()
            
        return price_per_night * duration
    
    @staticmethod
    def get_invoice(session,email):
        invoice_query = session.query(Invoice.amount,Invoice.price_per_night,Guest.email,Booking.booked_duration)\
            .join(Guest ,Invoice.guest_id==Guest.id)\
            .join(Booking, Invoice.booking_id==Booking.id)\
            .where(Invoice.expired==False)\
            .where(Invoice.paid==False)\
            .where(Guest.email==email)\
            .all()
        
        invoice_string = ""
        for amount, price, guest, days in invoice_query:
            invoice_string+=f"{guest} bokade {days} dagar för {str(price)}/dag. Total: {str(amount)}kr\n"
        return invoice_string
    
            
    @staticmethod
    def create_invoice(session, email, room_number, amount)  -> None:
        '''Finds guest_id using email and room_id using room_number
        '''
        guest_id = session.query(Guest.id)\
            .where(Guest.email==email)\
            .scalar()
        
        booking_id = session.query(Booking.id)\
            .order_by(Booking.created_at.desc())\
            .limit(1)\
            .scalar()
        
        
        price_per_night = session.query(Room.price_per_night)\
            .where(Room.room_number==room_number)\
            .scalar()
            

        new_invoice = Invoice(
            amount=amount,
            guest_id=guest_id,
            booking_id=booking_id,
            paid=False,
            price_per_night=price_per_night,
            expired=False)

        session.add(new_invoice)
        session.commit()