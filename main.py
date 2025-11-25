from sqlalchemy import create_engine, func, select

from sqlalchemy.orm import Session

from database.db import My_Session
from models.base import Base
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
            
             
        session.commit()
        
        session.close()
    
    # while True:
    #     try:
    #         choice = int(input("Lindas Lustfyllda Hotell & Pensionat\n=====================\nVal:\n1. Boka rum\n2.Avboka rum\n3. Statistik meny"))
    #     except(ValueError):
    #         print("Ange ett av befintliga val")

    #     if choice == 1:
    #         pass
        
    #     if choice == 2:
    #         pass
        
    #     if choice == 3:
    #         pass
        
        
if __name__ == "__main__":
    main()