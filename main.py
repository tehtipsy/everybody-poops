from auth import auth_menu, logout
from init import init_main_menu as init_main_menu

def show_main_menu():
    print("\n\n\n------------MAIN--MENU-------------")
    print('Welcome to the "Everybody Poops" app!')
    print("Please select an option:")
    print("0. Exit")
    print("1. Log an Entry")
    print("2. View Entry History")
    print("3. Edit Entry")
    print("4. Export History")
    print("5. Load History")
    print("-----------------------------------")

def main():

    edit_entry, log_entry, export_history, view_history, load_history = init_main_menu().values()

    while True:
        show_main_menu()
        choice = input("\nChoose Option: ")
        
        if choice == '1':
            # Create entry for a new entry
            log_entry()
        elif choice == '2':
            # View entries history
            view_history()
        elif choice == '3':
            # Edit entry
            edit_entry()
        elif choice == '4':
            # Export history
            export_history()
        elif choice == '5':
            # Load history
            load_history()
        elif choice == '0':
            # Exit or logout
            choice = input("Do you want to exit or logout? (e/l): ")
            if choice.lower() == 'e':
                print("Goodbye!")
                break
            # Logout and return to auth menu
            elif choice.lower() == 'l':
                logout()
                user = auth_menu()
                if not user:
                    print("Goodbye!")
                    break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    # Init with login menu and only show main menu if login is successful
    user = auth_menu()
    if user:
        main()
    else:
        print("Goodbye!")