from models.booking import Booking
from database.db import My_Session
from functions import check_month

session = My_Session()

def menu_interface():
    while True:
        try:
            choice = int(input("Lindas Lustfyllda Hotell & Pensionat\n=====================\nVal:\n1. Boka rum\n2. Avboka rum\n3. Statistik meny\n"))


            if choice == 1:
                month = int(input("Vilken månad vill du kolla 1-12\n"))
                booked_dates = Booking.show_available_dates(session)
                check_month(month,booked_dates,session)
                
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
        
