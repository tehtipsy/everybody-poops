from datetime import datetime, timedelta

# Sample data to use when no saved file exists
def get_dummy_logs():
    now = datetime.now()
    return [
        {"id": 1, "type": "1", "notes": "Morning routine",   "timestamp": str(now - timedelta(days=2))},
        {"id": 2, "type": "2", "notes": "Post-lunch",         "timestamp": str(now - timedelta(days=1))},
        {"id": 3, "type": "1", "notes": "Before bed",         "timestamp": str(now - timedelta(hours=6))},
    ]

