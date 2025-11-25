def menu():
    while True:
        try:
            choice = int(input("Lindas Lustfyllda Hotell & Pensionat\n=====================\nVal:\n1. Boka rum\n2.Avboka rum\n3. Statistik meny"))
        except(ValueError):
            print("Ange ett av befintliga val")

        if choice == 1:
            pass
        
        if choice == 2:
            pass
        
        if choice == 3:
            break