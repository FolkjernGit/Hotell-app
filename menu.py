from models.booking import Booking
from database.db import My_Session
from functions import check_user
from models.room import Room

session = My_Session()

def menu_interface():
    while True:
        try:
            choice = int(input("Lindas Lustfyllda Hotell & Pensionat\n=====================\nVal:\n1. Boka rum\n2. Avboka rum\n3. Statistik meny\n"))


            if choice == 1:
                new_guest = str(input("Enter email\n"))
                if check_user(session,new_guest):
                    print("Guest email already exists")
                
                print("Vilket rum vill du boka")
                existerande_room = Room.get_rooms(session)
                for room in existerande_room:
                    print(f"Room number {room[0]} Room count: {room[1]} Price per night {room[2]}")
                    
                room = int(input(f"Ange nummer 1 - {len(existerande_room)}"))
                month = int(input("Vilken månad vill du kolla 1-12\n"))
                bajs = Booking.check_rooms(session,month,existerande_room[3])
                
                for b in bajs:
                    print(b)
                
            elif choice == 2:
                pass
            
            elif choice == 3:
                pass
            
            elif choice == 4:
                break
            
            else:
                print("Ange nummer 1-4")
                
        except(ValueError):
            print("Ogiltig input")
        
