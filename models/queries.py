
from sqlalchemy import func

from models.booking import Booking
from models.guest import Guest
from models.invoice import Invoice


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
        .order_by(func.sum(Invoice.amount))\
        .group_by(Guest.id, Guest.first_name)\
        .all()
    booking_stats = "Mest spenderat"
    for name, amount in query:
        booking_stats += f"\n{name}: {amount} spenderat"
    
    return booking_stats