
from menu import menu
from database.db import My_Session

from models.guest import Guest
from models.room import Room



def main():
    
    with My_Session() as session:
        # Seeding
        count = session.query(Guest).count()
        if count == 0:
            guests = Guest.create_seeding()
            session.add_all(guests)
        
        
        count = session.query(Room).count()
        if count == 0:
            rooms = Room.create_seeding()  
            session.add_all(rooms) 
            
        menu()
        
        session.commit()
        
        session.close()
    

        
        
if __name__ == "__main__":
    main()