
from sqlalchemy import func, String, text

from models.booking import Booking
from models.guest import Guest
from models.invoice import Invoice
from models.room import Room


def get_booking_stats(session):
    query = session.query(func.count(Booking.id),Guest.first_name)\
        .join(Guest, Booking.guest_id == Guest.id)\
        .where(Guest.is_deleted==False)\
        .order_by(func.count(Booking.id).desc())\
        .group_by(Guest.id, Guest.first_name)\
        .all()
    booking_stats = "Boknings statistik"
    for count, name in query:
        booking_stats += f"\n{name}: {count} bokningar"    

    return booking_stats


def get_total_spent(session):
    query = session.query(Guest.first_name,func.sum(Invoice.amount))\
        .join(Guest, Invoice.guest_id == Guest.id)\
        .where(Guest.is_deleted==False)\
        .order_by(func.sum(Invoice.amount).desc())\
        .group_by(Guest.id, Guest.first_name)\
        .all()
    booking_stats = "Mest spenderat"
    for name, amount in query:
        booking_stats += f"\n{name}: {amount} spenderat"
    
    return booking_stats



def get_most_booked(session, from_date, to_date):
    end_date = func.timestampadd(
        text("DAY"),            
        Booking.booked_duration,
        Booking.book_date)

    query = session.query(Room.room_number, func.count(Booking.id))\
        .join(Booking, Booking.room_id == Room.id)\
        .where(Booking.book_date <= to_date, end_date >= from_date)\
        .group_by(Room.id, Room.room_number)\
        .order_by(func.count(Booking.id).desc())\
        .all()


    stats = f"Mest bokade rum mellan {from_date} och {to_date}"
    for room, count in query:
        stats += f"\nRum {room}: {count} bokningar"

    return stats
