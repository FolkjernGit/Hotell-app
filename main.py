from menu import menu_interface
from database.db import My_Session
from functions import seeding


def main():
    
    with My_Session() as session:

        seeding(session)
        
        menu_interface()
        
        session.close()

if __name__ == "__main__":
    main()