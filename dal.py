import json
import csv
import os
import secrets
from dummy_data import get_dummy_logs

# Config
DATA_DIR  = os.path.dirname(os.path.abspath(__file__))

# This will hold the in-memory logs list, initialized from load_logs()
logs = []  

def _build_file_path(filename, extension):
    """
    Build a file path in the project data directory.
    Adds the expected extension if the user omitted it.
    """
    cleaned_name = filename.strip()
    if not cleaned_name:
        raise ValueError("Filename cannot be empty.")

    if not cleaned_name.lower().endswith(f".{extension}"):
        cleaned_name = f"{cleaned_name}.{extension}"

    return os.path.join(DATA_DIR, cleaned_name)


def _load_json_logs(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        for entry in data:
            entry["id"] = str(entry["id"]).upper()
        return data


def _load_csv_logs(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        for entry in data:
            entry["id"] = str(entry["id"]).upper()
        return data

# Load
def load_logs():
    """
    Load logs from a user-selected JSON or CSV file,
    or fall back to dummy data.
    """
    while True:
        choice = input("\nChoose import format (1 for JSON, 2 for CSV, 0 for dummy data): ").strip()

        if choice == "0":
            print("[DAL] Using dummy data.")
            choice = input("[DAL] Append dummy data or replace existing logs? (a/r): ").strip().lower()
            if choice == "a":
                return logs + get_dummy_logs()
            elif choice == "r":
                return get_dummy_logs()

        if choice not in ["1", "2"]:
            print("Invalid choice. Please try again.")
            continue

        filename = input("Enter file name (without or with extension): ").strip()
        if not filename:
            print("Filename cannot be empty. Please try again.")
            continue

        extension = "json" if choice == "1" else "csv"
        file_path = _build_file_path(filename, extension)

        if not os.path.exists(file_path):
            print(f"[DAL] File not found: {file_path}")
            continue

        try:
            if choice == "1":
                data = _load_json_logs(file_path)
            else:
                data = _load_csv_logs(file_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"[DAL] Failed to load file: {error}")
            continue

        if len(logs) > 0:
            choice = input("[DAL] Append loaded data to existing logs? (y/n): ").strip().lower()
            if choice == "y":
                return logs + data
        print(f"[DAL] Loaded logs from {file_path}")
        return data

# Save
def save_logs_json(filename):
    """
    Export the current list to a JSON file.
    """
    file_path = _build_file_path(filename, "json")

    with open(file_path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"[DAL] Saved {len(logs)} entries to {file_path}")

def save_logs_csv(filename):
    """
    Export the current logs list to a CSV file.
    """
    if not logs:
        print("[DAL] Nothing to save.")
        return

    file_path = _build_file_path(filename, "csv")

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=logs[0].keys())
        writer.writeheader()
        writer.writerows(logs)
    print(f"[DAL] Saved {len(logs)} entries to {file_path}")

# Helper - 4-character hex ID generator
def new_unique_id():
    """
    Return a unique 4-character hexadecimal ID string.
    """
    existing_ids = {str(entry["id"]) for entry in logs}

    if len(existing_ids) >= 16 ** 4:
        raise ValueError("No 4-character hexadecimal IDs remaining.")

    while True:
        new_id = f"{secrets.randbelow(16 ** 4):04X}"
        if new_id not in existing_ids:
            return new_id

# The shared logs list (single source of truth)
logs = load_logs()
