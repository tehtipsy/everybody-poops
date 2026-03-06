import json
import csv
import os
from dummy_data import get_dummy_logs

# Config
DATA_DIR  = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(DATA_DIR, "logs.json")
CSV_FILE  = os.path.join(DATA_DIR, "logs.csv")

# Load
def load_logs():
    """
    Load logs from JSON, CSV file, 
    or fall back to dummy data.
    """
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            print(f"[DAL] Loaded logs from {JSON_FILE}")
            return json.load(f)

    # If no JSON file, try CSV
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
            # csv reads everything as strings — convert id back to int
            for entry in data:
                entry["id"] = int(entry["id"])
            print(f"[DAL] Loaded logs from {CSV_FILE}")
            return data

    print("[DAL] No saved file found — using dummy data.")
    return get_dummy_logs()

# Save ---
def save_logs_json():
    """
    Export the current list to a JSON file.
    """
    with open(JSON_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"[DAL] Saved {len(logs)} entries to {JSON_FILE}")

def save_logs_csv():
    """
    Export the current logs list to a CSV file.
    """
    if not logs:
        print("[DAL] Nothing to save.")
        return
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=logs[0].keys())
        writer.writeheader()
        writer.writerows(logs)
    print(f"[DAL] Saved {len(logs)} entries to {CSV_FILE}")

# Helper - Next ID generator
def next_id():
    """
    Return the next available ID.
    """
    if not logs:
        return 1
    return max(int(entry["id"]) for entry in logs) + 1

# The shared logs list (single source of truth)
logs = load_logs()