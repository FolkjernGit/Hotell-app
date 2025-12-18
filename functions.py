import calendar
from datetime import datetime, timedelta
from random import choice, randint
import uuid
from models.guest import Guest
from models.invoice import Invoice
from models.room import Room

from typing import List
from models.booking import Booking




from random import choice, randint
import uuid
import calendar
from datetime import datetime

def seeding(session):
    # Seed guests
    if session.query(Guest).count() == 0:
        guests = Guest.create_seeding()
        session.add_all(guests)

    # Seed rooms
    if session.query(Room).count() == 0:
        rooms = Room.create_seeding()
        session.add_all(rooms)

    session.commit()  # commit guests and rooms first

    # Prepare for booking seeding
    bookings = []
    invoices = []

    rooms = session.query(Room).all()
    guests = session.query(Guest).all()
    room_dict = {r.id: (r.room_number, r.price_per_night) for r in rooms}
    guest_ids = [g.id for g in guests]

    
    bookings_per_month = 2

    for month in range(1, 13):
        year = 2025
        _, num_days = calendar.monthrange(year, month)

        for _ in range(bookings_per_month):
            year = randint(2020,2025)
            room_id = choice(list(room_dict.keys()))
            guest_id = choice(guest_ids)
            duration = randint(1, 5)
            people = randint(1, 4)
            start_day = randint(1, num_days - duration + 1)
            start_date = datetime(year, month, start_day)
            booking_id = str(uuid.uuid4())

            # Create booking
            booking = Booking(
                id=booking_id,
                room_id=room_id,
                guest_id=guest_id,
                book_date=start_date,
                booked_duration=duration,
                people=people
            )
            bookings.append(booking)

            # Get room info from pre-fetched dict
            room_number, price_per_night = room_dict[room_id]

            # Compute amount
            amount = Invoice.get_amount(session,duration=duration, room_number=room_number, people=people)

            # Create invoice
            invoice = Invoice(
                amount=amount,
                guest_id=guest_id,
                booking_id=booking_id,
                price_per_night=price_per_night,
                paid=False,
                expired=False
            )
            invoices.append(invoice)

    # Add all bookings and invoices at once
    session.add_all(bookings + invoices)
    session.commit()


def check_user(session,email) -> bool:
    '''if user exists
        return True else False
    '''
    emails: List[str] = [r[0] for r in session.query(Guest.email).where(Guest.is_deleted==False).all()]
    
    if email in emails:
        return True
    
    return False
        
def get_invoices(session):
    invoices = session.query(Invoice).all()
    return invoices

def check_expired_bookings(session):
    expired_bookings = session.query(Booking).all()
    expired_bookings = [
        b for b in expired_bookings
        if b.book_date + timedelta(days=b.booked_duration) < datetime.now()
    ]
    for booking in expired_bookings:
        booking.people = 999  # Mark as expired
        session.commit()  

            