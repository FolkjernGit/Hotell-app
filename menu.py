from models.booking import Booking
from database.db import My_Session
from functions import check_user
from models.room import Room
import calendar

session = My_Session()

def menu_interface():
    while True:
        try:
            choice = int(input("Lindas Lustfyllda Hotell & Pensionat\
                \n       --Val--\n=====================\n| 1. Boka rum       |\
                    \n| 2. Avboka rum     |\n| 3. Statistik meny |\n| 4. Avsluta        |\
                        \n=====================\n> "))
        except ValueError:
            print("Välj ett av valen ovan!")
            continue

        if choice == 1:
            new_guest = str(input("Enter email\n"))
            if check_user(session,new_guest):
                print(f"Bokar rum åt addressen '{new_guest}'")
            else:
                pass # TODO lägg till nu användare
            print("Vilket rum vill du boka:")
            existerande_room = Room.get_rooms(session)
            for room in existerande_room:
                print(f"Room number {room[0]} Room count: {room[1]} Price per night {room[2]}")
                
            room = int(input(f"Ange rum nummer 1 - {len(existerande_room)}\n> "))
            
            month = int(input("Vilken månad vill du boka: 1-12\n> "))
            selected_room_id = session.query(Room.id).where(Room.room_number==room).scalar()
            checked_month, booked_dates = Booking.check_rooms(session,month,selected_room_id)
            
            for date in checked_month:
                print(date)
                
            choose_date = int(input("Välj en dag som startdatum\n > "))
            choose_duration = 1
            if choose_date in booked_dates:
                print("Datumet är redan bokat!")
                continue
            
            elif choose_date <= len(checked_month) or choose_date >= 1:
                choose_duration = int(input("Hur många dagar vill du boka?\n> "))
                for date in range(choose_date, choose_date+choose_duration):
                    if date in booked_dates:
                        print("Datumet är redan bokat!")
                        break
            else:
                print("idk what u did man")
            
            confirm = str(input(f"Bekräfta bokning för {new_guest} {calendar.month_name[month]}\
                  dag {choose_date} till {choose_date+choose_duration-1}\nJ/N\n> "))
            
            if confirm == "J".upper():
                pass
            else:
                continue
            
        elif choice == 2:
            pass
        
        elif choice == 3:
            pass
        
        elif choice == 4:
            break
        
        else:
            print("Ange nummer 1-4")
            

    
