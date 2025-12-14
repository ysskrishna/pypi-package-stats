from datetime import date


def get_last_30_days_data(data: list) -> list:
    """Filter data to last 30 days"""
    cutoff = date.today().replace(day=1)  # First day of current month
    return [d for d in data if d["date"] >= cutoff.isoformat()]


def aggregate_by_category(data: list) -> dict:
    """Aggregate downloads by category"""
    totals = {}
    for row in data:
        cat = row["category"]
        totals[cat] = totals.get(cat, 0) + row["downloads"]
    return totals

