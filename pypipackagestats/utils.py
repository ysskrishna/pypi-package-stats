from datetime import datetime, date
from pathlib import Path
import platformdirs


def humanize_number(num: int) -> str:
    """Convert large numbers to human-readable format (K, M, B)"""
    for unit in ['', 'K', 'M', 'B']:
        if abs(num) < 1000:
            return f"{num:,.1f}{unit}".rstrip('0').rstrip('.')
        num /= 1000
    return f"{num:,.1f}T"


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


def normalize_os_name(os_name: str) -> str:
    """Normalize OS names for display"""
    if not os_name:
        return "other"
    mapping = {
        "darwin": "macOS",
        "windows": "Windows",
        "linux": "Linux"
    }
    return mapping.get(os_name.lower(), os_name.title() or "other")


def get_cache_dir() -> Path:
    """Get cache directory for diskcache (platform-specific)"""
    cache_dir = Path(platformdirs.user_cache_dir("pypipackagestats", "pypipackagestats"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

