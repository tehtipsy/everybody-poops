import json
import os
import hashlib

# Config for users persistence
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Internal helpers
def _hash_password(password):
    """
    Hash a password using SHA-256 for demo.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users():
    """
    Load users from the JSON file, 
    or return empty dict.
    """
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_users(users):
    """
    Persist users dict to JSON file.
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Public API
def register():
    """
    Register a new user with a username and password.
    """
    users = _load_users()
    username = input("Choose a username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return None

    if username in users:
        print("Username already taken.")
        return None

    password = input("Choose a password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return None

    users[username] = _hash_password(password)
    _save_users(users)
    print(f"\nUser '{username}' registered successfully!")
    return username

def login():
    """
    Authenticate an existing user. 
    Returns username on success, None on failure.
    """
    users = _load_users()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in users:
        print("\nUser not found.")
        return None

    if users[username] != _hash_password(password):
        print("\nIncorrect password.")
        return None

    print(f"\nWelcome back, {username}!")
    return username

def display_auth_menu():
    """
    Display the "login or register" menu.
    """
    print("\n========= LOGIN =========")
    print("1. Login")
    print("2. Register")
    print("0. Exit")
    print("=========================")

def auth_menu():
    """
    Show login/register menu. 
    Returns the authenticated username, or None to quit.
    """
    while True:
        display_auth_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = login()
            if user:
                return user
        elif choice == "2":
            user = register()
            if user:
                return user
        elif choice == "0":
            return None
        else:
            print("Invalid option.")
