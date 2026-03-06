from datetime import datetime, timedelta


def _generate_dummy_ids(count):
    from dal import new_unique_id

    ids = set()
    while len(ids) < count:
        ids.add(new_unique_id())
    return list(ids)

# Sample data to use when no saved file exists
def get_dummy_logs():
    now = datetime.now()
    dummy_ids = _generate_dummy_ids(3)
    return [
        {"id": dummy_ids[0], "type": "1", "notes": "Morning routine", "timestamp": str(now - timedelta(days=2))},
        {"id": dummy_ids[1], "type": "2", "notes": "Post-lunch", "timestamp": str(now - timedelta(days=1))},
        {"id": dummy_ids[2], "type": "1", "notes": "Before bed", "timestamp": str(now - timedelta(hours=6))},
    ]

