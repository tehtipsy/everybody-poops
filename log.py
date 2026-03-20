from datetime import datetime
from dal import logs, new_unique_id

def _check_size(size):
    """
    Checks the size of the number 2 and returns a message 
    based on the size compared to the worldwide average.    
    """
    if 2 <= size <= 4:
        message = "\n\nYour number 2 diameter is within the worldwide average"
    elif size > 4:
        message = "\n\nYour number 2 diameter is bigger then worldwide average, well done!"
    elif size < 2 and size != 0:
        message = "\n\nYour number 2 diameter is smaller then worldwide average, ):"

    return message

def _ask_for_size():
    """
    Asks the user for the size of their number 2 and checks it against the worldwide average.
    """
    size = 0

    raw_size = input("Type 2 selected, please enter the diameter of your type 2 in cm (optional): ")

    if raw_size == "":
        size = 0
    else:
        try:
            size = int(raw_size)
        except ValueError:
            size = 0

    return _check_size(size)

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

    # added a small check if the user selected number 2, if they did ask them 
    # for number 2 size, and display a message if the size is within the worldwide average or not
    message = None

    if type == "2":
        message =_ask_for_size()

    notes = input("Enter any notes (optional): ")

    # printing message after enter any notes for consistency 
    if message is not None:
        print(message)

    return {
        "id": new_unique_id(),
        "type": type,
        "notes": notes,
        "timestamp": str(datetime.now())
    }

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
            # Retry if entry creation failed
            return log_entry()  

        logs.append(entry)
        print("\n\nEntry logged successfully!")

        choice = input("\nLog another entry? (y/n): ")
        if choice.lower() != 'y':
            break

        # Else, loop again to log another entry
        return log_entry()