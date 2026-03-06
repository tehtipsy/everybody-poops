from dal import save_logs_csv, save_logs_json

def export_history():
    """
    Exports the history to a file.
    This function would typically ask the user for a file name and format (e.g., CSV, JSON) 
    and then save the history in that format.
    """
    while True:
        choice = input("\nChoose export format (1 for JSON, 2 for CSV): ")

        if choice not in ["1", "2"]:
            print("Invalid choice. Please try again.")
            continue

        filename = input("Enter file name (without or with extension): ").strip()
        if not filename:
            print("Filename cannot be empty. Please try again.")
            continue

        print("\nExporting history...")
        if choice == "1":
            save_logs_json(filename)
        else:
            save_logs_csv(filename)
        break
