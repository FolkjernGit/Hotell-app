from tokenize import String
from sqlalchemy import func
from models.booking import Booking
from database.db import My_Session
from functions import check_user, get_invoices, read_date
from models.guest import Guest
from models.invoice import Invoice
from queries import get_booking_stats, get_total_spent
from models.room import Room
import calendar
from datetime import datetime
import time

session = My_Session()

def menu_interface():
    while True:
        try:
            choice = int(input(
                "Lindas Lustfyllda Hotell & Pensionat"
                "\n        -- Val --"
                "\n====================="
                "\n| 1. Boka rum       |"
                "\n| 2. Betala faktura |"
                "\n| 3. Statistik meny |"
                "\n| 4. Admin meny     |"
                "\n| 5. Avsluta        |"
                "\n====================="
                "\n> "
            ))
        except ValueError:
            print("Välj ett av valen ovan!")
            continue

        if choice == 1:
            email = str(input("Enter email\n"))
            if check_user(session,email):
                print(f"Bokar rum åt addressen '{email}'")
            elif len(email) > 255
                print("Email för lång!")
                continue
            else:
                print("Ny användare!")
                while True:
                    try:
                        fullname = str(input("Fyll i förnamn <space> efternamn\n"))
                        if len(fullname.split()) != 2 or len(fullname.split()[0]) > 255 or len(fullname.split()[1]) > 255:
                            print("Fel format skriv: förnamn <space> efternamn")
                            continue
                        
                    except ValueError:
                        print("Namn kan inte ha siffror eller andra tecken!")

                    Guest.add_guest(session,fullname,email)
                    print(f"La till användaren {email}, med namn {fullname.capitalize()}")
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
                amount = Invoice.get_amount(session,choose_duration,room_number,people)
                Booking.create_booking(session,room_number,email,choose_date,choose_duration,month,people)
                Invoice.create_invoice(session,email,room_number,amount)
                print(f"Bokning genomförd för {email} faktura skickad")
                time.sleep(0.8)
            else:
                continue
            
        elif choice == 2:
            try:
                email = str(input("Enter email\n"))
            except ValueError:
                print("Ogiltig input!")
                continue
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
            while True:
                print(
                    "\n--- Statistik meny ---"
                    "\n1. Bokningar per gäst"
                    "\n2. Mest spenderat per gäst"
                    "\n3. Mest bokade rum (datumintervall)"
                    "\n4. Avsluta"
                )
        
                try:
                    stat_choice = int(input("> "))
                except ValueError:
                    print("Välj ett nummer 1–4")
                    continue
        
                if stat_choice == 1:
                    print(get_booking_stats(session))
        
                elif stat_choice == 2:
                    print(get_total_spent(session))
        
                elif stat_choice == 3:
                    start = read_date("Startdatum (YYYY-MM-DD): ")
                    end = read_date("Slutdatum (YYYY-MM-DD): ")
        
                    if start > end:
                        print("Startdatum kan inte vara efter slutdatum")
                        continue
        
                    print(get_most_booked(session, start, end))
        
                elif stat_choice == 4:
                    break
        
                else:
                    print("Ogiltigt val")
        elif choice == 4:
            choice = int(input("ADMIN MENY\n1. Ändra boking\n2. Ändra kund info\n3. Ta bort kund\n> "))
            if choice == 1:
                try:
                    email = str(input("Ange email för användare\n> "))
                except ValueError:
                    print("Ogiltig input")
                    continue
                if not check_user(session,email):
                    print("Användare finns inte!")
                    continue
                guest_id = session.query(Guest.id).where(Guest.email==email).scalar()
                bookings = session.query(Booking).where(Booking.guest_id==Guest.id)\
                    .where(Booking.people < 999).all()
                for booking in bookings:
                    print(f"Bokning id: {booking.id} Rum id: {booking.room_id} Start datum: {booking.book_date} Antal dagar: {booking.booked_duration} Antal personer: {booking.people}")
                booking_id = str(input("Ange boknings id att ändra\n> "))
                booking = session.query(Booking).where(Booking.id==booking_id).first()  
                choice = str(input("1. Lägg till dagar\n2. Ändra antal personer\n> "))
                if choice == "1":
                    invalid = False
                    try:
                        extra_days = int(input("Hur många extra dagar vill du lägga till?\n> "))
                    except ValueError:
                        print("Ogiltig input")
                        continue
                    free_dates,_ = Booking.check_rooms(session,booking.book_date.month,booking.room_id)
                    for date in range(booking.book_date.day, booking.book_date.day + booking.booked_duration + extra_days):
                        if booking.book_date.day + booking.booked_duration + extra_days -1 not in free_dates:
                            print("Kan inte lägga till dagar, datum är redan bokat!")
                            invalid = True
                            break
                    if invalid:
                        continue
                    booking.booked_duration += extra_days
                    session.commit()
                elif choice == "2":
                    try:
                        new_people = int(input("Ange nytt antal personer 1-4\n> "))
                    except ValueError:
                        print("Ogiltig input")
                        continue
                    if new_people < 1 or new_people > 4:
                        print("Max 4 personer per rum!")
                        continue
                    booking.people = new_people
                    session.commit()
                    
            elif choice == 2:
                try:
                    email = str(input("Ange email för användare\n> "))
                except ValueError:
                    print("Ogiltig input")
                if check_user(session,email):
                    while True:
                        try:
                            fullname = str(input("Fyll i förnamn <space> efternamn\n"))
                            if len(fullname.split()) != 2:
                                print("Fel format skriv: förnamn <space> efternamn")
                                continue
                            
                        except ValueError:
                            print("Namn kan inte ha siffror eller andra tecken!")
                        f_name, l_name = fullname.split()
                        guest = session.query(Guest).where(Guest.email==email).first()
                        guest.first_name = f_name.capitalize()
                        guest.last_name = l_name.capitalize()

                        session.commit()
                        print("Namn ändrat!")
                        break
                else:
                    print("Användare finns inte!")
            elif choice == 3:
                try:
                    email = str(input("Ange email för användare\n> "))
                except ValueError:
                    print("Ogiltig input")
                if not check_user(session,email):
                    print("Användare finns inte!")
                    continue
                guest_id = session.query(Guest.id).where(Guest.email==email).scalar()
                if session.query(Booking)\
                    .where(Booking.people < 999)\
                    .where(Booking.guest_id==guest_id)\
                    .all():
                    print("Användaren har aktiva bokningar, kan inte ta bort!")
                    continue
                guest = session.query(Guest).where(Guest.email==email).first()
                guest.is_deleted = True
                session.commit()
                print("Användare borttagen!")

            else:
                pass
        elif choice == 5:
            break
        else:
            print("Ange nummer 1-4")
            
