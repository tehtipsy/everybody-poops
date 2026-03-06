from dal import logs

def find_entry_by_id(id):
    """
    Helper function to find a log entry by its ID.
    Returns the entry if found, or None if not found.
    """
    # Using built in next function to find the first matching entry or return None
    return next((log for log in logs if log.get("id") == id), None)

def update_entry(entry):
    """
    Helper function to update an existing log entry.
    Prompts the user for new values for the entry's fields and updates them.
    """
    new_type = input(f"Enter new type (current: {entry['type']}): ")
    if new_type in ["1", "2"]:
        entry["type"] = new_type
    else:
        print("Invalid type. Type not updated.")

    new_notes = input(f"Enter new notes (current: {entry['notes']}, press enter to skip): ")
    if new_notes:
        entry["notes"] = new_notes

    print("Entry updated successfully!")

def edit_entry():
    """
    Allows the user to edit an existing entry.
    Asks the user for the ID of the entry they want to edit, 
    checks if it exists, 
    and then allows them to update the details of that entry.
    """
    while True:
        id = int(input("Enter the ID of the entry you want to edit: "))

        # Check if the entry exists
        entry = find_entry_by_id(id)

        if entry is None:
            print(f"No entry found with ID: {id}")
            # Retry if entry not found
            return edit_entry()  

        print(f"Editing entry: {entry}")

        retry = input("\nDo you want to:\n - edit this entry (y or any other input)\n - try another ID (n)\n - return to main menu (e)\n(y/n/e): ")
        if retry.lower() == 'n':
            return edit_entry()
        elif retry.lower() == 'e':
            print("Returning to menu.")
            return

        print(f"\nProceeding to edit entry with ID: {entry['id']}\n")

        # Update the entry details
        update_entry(entry)

        exit = input("\nDo you want to return to the menu? (y/n): ")
        if exit.lower() == 'y':
            print("Returning to menu.")
            break