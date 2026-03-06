from dal import logs, load_logs

def print_rows(rows):
    """
    Helper function to print a list of log entries in a readable format.
    """
    for row in rows:
        print(f" - ID: {row['id']}, Type: {row['type']}, Notes: {row['notes']}, Timestamp: {row['timestamp']}")

def view_history():
    """
    Displays the history of entries to the user.
    """
    while True:    
        print("\nViewing history...\n")
        if not logs:
            print("No entries found.")
            return

        print_rows(logs)

        choice = input("\nReturn to menu? (y/n): ")
        if choice.lower() == 'y':
            break
        print("Invalid choice. Please try again.")

def load_history():
    """
    Loads history from a file and updates the in-memory logs.
    """
    print("\nLoading history...")
    new_logs = load_logs()
    if new_logs is not None:
        logs.clear()
        logs.extend(new_logs)
        print(f"Loaded {len(new_logs)} entries into history.")