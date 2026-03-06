from datetime import datetime
from dal import logs, next_id

def create_log_entry():
    """
    Creates a new log entry.
    Asks the user for details about the entry (e.g., type, notes) 
    and returns the entry as a dictionary.
    """
    type = input("Enter the type (1 or 2): ")

    if type not in ["1", "2"]:
        print("Invalid type. Entry not created.")
        return None

    notes = input("Enter any notes (optional): ")

    entry = {
        "id": next_id(),
        "type": type,
        "notes": notes,
        "timestamp": str(datetime.now())
    }

    return entry

def log_entry():
    """
    Logs a new entry.
    and saves it to the history.
    """
    while True:
        print("Logging a new entry...")
        # Save Entry with auto-generated ID and timestamp
                
        # Save the entry to the history
        entry = create_log_entry()
        if entry is None:
            return log_entry()  # Retry if entry creation failed
        
        logs.append(entry)
        print("\n\nEntry logged successfully!")
        
        choice = input("\nLog another entry? (y/n): ")
        if choice.lower() != 'y':
            break
        
        # else, loop again to log another entry
        return log_entry()