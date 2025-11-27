from models.guest import Guest
from models.room import Room




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