from models.room import Room
from database.db import My_Session

session = My_Session()

def menu_interface():
    while True:
        try:
            choice = int(input("Lindas Lustfyllda Hotell & Pensionat\n=====================\nVal:\n1. Boka rum\n2. Avboka rum\n3. Statistik meny\n"))


            if choice == 1:
                print(Room.show_avaible_rooms(session))
                bajs = str(input("Vilket rum vill du boka?\n"))
                
                
            if choice == 2:
                pass
            
            if choice == 3:
                break
            
        except(ValueError):
            print("Ange ett av befintliga val")