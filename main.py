from edit import edit_entry
from log import log_entry
from export import export_history
from view import view_history
from auth import auth_menu

def show_main_menu():
    print("\n\n\n------------MAIN--MENU-------------")
    print('Welcome to the "Everybody Poops" app!')
    print("Please select an option:")
    print("0. Exit")
    print("1. Log an Entry")
    print("2. View Entry History")
    print("3. Edit Entry")
    print("4. Export History")
    print("-----------------------------------")

def main():
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
        elif choice == '0':
            # Exit
            choice = input("Are you sure you want to exit? (y/n): ")
            if choice.lower() == 'y':
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