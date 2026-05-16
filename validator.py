from datetime import datetime

REQUIRED_FIELDS = {"date", "category", "description", "amount", "budget"}


def validate_transaction(row):
    if not REQUIRED_FIELDS.issubset(row.keys()):
        return False
    try:
        datetime.strptime(row["date"], "%Y-%m-%d")
        float(row["amount"])
        float(row["budget"])
    except (TypeError, ValueError):
        return False
    return bool(row["category"] and row["description"])
