from models.booking import Booking
from database.db import My_Session
from functions import check_user, get_invoices
from models.guest import Guest
from models.invoice import Invoice
from models.queries import get_booking_stats, get_total_spent
from models.room import Room
import calendar
from datetime import datetime
import time

session = My_Session()

def menu_interface():
    while True:
        try:
            choice = int(input("Lindas Lustfyllda Hotell & Pensionat\
                \n       --Val--\n=====================\n| 1. Boka rum       |\
                    \n| 2. Betala faktura |\n| 3. Statistik meny |\n| 4. Avsluta        |\
                        \n=====================\n> "))
        except ValueError:
            print("Välj ett av valen ovan!")
            continue

        if choice == 1:
            email = str(input("Enter email\n"))
            if check_user(session,email):
                print(f"Bokar rum åt addressen '{email}'")
            else:
                print("Ny användare!")
                while True:
                    try:
                        fullname = str(input("Fyll i förnamn <space> efternamn\n"))
                        if len(fullname.split()) != 2:
                            print("Fel format skriv: förnamn <space> efternamn")
                            continue
                        
                    except ValueError:
                        print("Namn kan inte ha siffror eller andra tecken!")

                    Guest.add_guest(session,fullname,email)
                    print(f"La till användaren {email}, med namn {fullname}")
                    break
                
            while True:
                print("Vilket rum vill du boka:")
                existerande_room = Room.get_rooms(session)
                for room in existerande_room:
                    print(f"Room number {room[0]} Room count: {room[1]} Price per night {room[2]}")
                
                
                try:
                    room_number = int(input(f"Ange rum nummer 1 - {len(existerande_room)}\n> "))
                except ValueError:
                    print("Välj ett giltigt nummer!")
                    continue
                if room_number < 1 or room_number > len(existerande_room):
                    print("Det rum numret finns inte!")
                    continue

                try:
                    month = int(input("Vilken månad vill du boka: 1-12\n> "))
                except ValueError:
                    print("Välj ett giltigt nummer!")
                    continue
                if month < 1 or month > 12:
                    print("Välj en riktig månad!")
                    continue
                else:
                    break
            
            selected_room_id = session.query(Room.id).where(Room.room_number==room_number).scalar()
            checked_month, booked_dates = Booking.check_rooms(session,month,selected_room_id)
            
            for date in checked_month:
                print(date)
            while True:
                try:
                    choose_date = int(input("Välj en dag som startdatum\n > "))
                except ValueError:
                    print("Välj ett giltigt datum!")
                    continue
                choose_duration = 1
                _, days_in_month = calendar.monthrange(datetime.now().year,month)
                if choose_date > days_in_month or choose_date < 1:
                    print("Välj ett datum i den här månaden!")
                    continue
                
                
                
                elif choose_date in booked_dates:
                    print("Datumet är redan bokat!")
                    continue
            
                elif choose_date <= len(checked_month) or choose_date >= 1:
                    choose_duration = int(input("Hur många dagar vill du boka?\n> "))
                    for date in range(choose_date, choose_date+choose_duration):
                        if date in booked_dates:
                            print("Datumet är redan bokat!")
                            continue
                    break
            while True:
                try:
                    people = int(input("Hur många personer 1-4\n"))
                except ValueError:
                    print("Ogiltig input!")
                if people > 4 or people < 1:
                    print("Max 4 gäster!")
                    continue
                break
            
            confirm = str(input(f"Bekräfta bokning för {email} {calendar.month_name[month]}\
                  dag {choose_date} till {choose_date+choose_duration-1}\nJ/N\n> "))
            
            if confirm == "J".upper():
                amount = Invoice.get_amount(session,choose_duration,room_number)
                Booking.create_booking(session,room_number,email,choose_date,choose_duration,month,people)
                Invoice.create_invoice(session,email,room_number,amount)
                print(f"Bokning genomförd för {email} faktura skickad")
                time.sleep(0.8)
            else:
                continue
            
        elif choice == 2:
            email = str(input("Enter email\n"))
            if not check_user(session,email):
                print("Användaren finns inte!")
                time.sleep(0.6)
                continue
            invoice_str = Invoice.get_invoice(session,email)
            if invoice_str == "":
                print("Användaren har ingen faktura att betala :)")
                time.sleep(0.6)
                continue
            print(invoice_str)
            pay = str(input("Betala faktura/fakturor\nJ/N\n"))
            if not pay == "J".upper():
                continue
            
            unpaid_invoices = Invoice.get_invoice_object(session,email)
            for invoice in unpaid_invoices:
                invoice.pay_invoice()
                session.commit()
                time.sleep(0.2)
                print(f"Betalning lyckades för {invoice.amount}kr")
            
        elif choice == 3:
            print(get_booking_stats(session))
            print(get_total_spent(session))
        elif choice == 4:
            break
        
        else:
            print("Ange nummer 1-4")
            