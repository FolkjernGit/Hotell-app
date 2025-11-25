from sqlalchemy import create_engine, func, select

from sqlalchemy.orm import Session

from database.db import My_Session
from models.base import Base
from models.guest import Guest
from models.room import Room



def main():
    
    with My_Session() as session:


        new_guest1 = Guest(first_name='Linus',last_name='Folkjern',email='folkjern@icloud.com')
        new_guest2 = Guest(first_name='Elin',last_name='Sjöberg',email='elin.sjoberg@example.com')
        new_guest3 = Guest(first_name='Marcus',last_name='Hallgren',email='marcus.hallgren@example.com')
        new_guest4 = Guest(first_name='Tilda',last_name='Bergström',email='tilda.bergstrom@example.com')

        session.add_all([new_guest1,new_guest2,new_guest3,new_guest4])
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