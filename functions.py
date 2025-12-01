from models.guest import Guest
from models.room import Room

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
    
    count = session.query(Booking).count()
    if count == 0:
        bookings = Booking.create_seeding(session)  
        session.add_all(bookings) 
    
    session.commit()

def check_user(session,email) -> bool:
    '''if user exists
        return True else False
    '''
    emails: List[str] = [r[0] for r in session.query(Guest.email).all()]
    
    if email in emails:
        return True
    
    return False
        
        

            