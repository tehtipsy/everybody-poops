from dal import logs, load_logs

def print_rows(rows):
    """
    Helper function to print a list of log entries in a readable format.
    """
    print("\nViewing history...\n")
    if not rows:
        print("No entries found.")
        return
    for row in rows:
        print(f" - ID: {row['id']}, Type: {row['type']}, Notes: {row['notes']}, Timestamp: {row['timestamp']}")

def view_history():
    """
    Displays the history of entries to the user.
    """
    while True:
        filter = input("""Choose a filter:
        1. All
        2. Poop
        3. Pee
        4. Filter by notes
        """)  

        logs_filtered = []
        if filter == "1":
            print_rows(logs)
        elif filter == "2":
            for log in logs:
                if log["type"] == "2":
                    logs_filtered.append(log)
            print_rows(logs_filtered)
        elif filter == "3":
            for log in logs:
                if log["type"] == "1":
                    logs_filtered.append(log)
            print_rows(logs_filtered)
        elif filter == "4":
            notes = input("Enter notes: ")
            for log in logs:
                if notes in log["notes"]:
                    logs_filtered.append(log)
            print_rows(logs_filtered)
        else:
            print("Invalid filter. Please try again.")
            continue

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