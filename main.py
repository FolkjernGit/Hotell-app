from menu import menu_interface
from database.db import My_Session
from functions import seeding
from models.invoice import Invoice

def main():
    
    with My_Session() as session:

        invoices = Invoice.get_invoice_object(session,0)
        for invoice in invoices:
            invoice.check_if_expired()
        
        seeding(session)

        menu_interface()
        
        session.close()
        
if __name__ == "__main__":
    main()