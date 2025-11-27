from models.guest import Guest
from models.room import Room
from datetime import datetime
from typing import List
from models.booking import Booking


def seeding(session):
   
    
    count = session.query(Guest).count()
    if count == 0:
        guests = Guest.create_seeding()
        session.add_all(guests)
    
    
    count = session.query(Room).count()
    if count == 0:
        rooms = Room.create_seeding()  
        session.add_all(rooms) 
    
    session.commit()
    
# TODO fix this
def check_month(month,booked_dates,session) -> List[datetime]:
    
    free_dates: List[datetime] = []
    for day in range():
        if day not in booked_dates:
            pass
