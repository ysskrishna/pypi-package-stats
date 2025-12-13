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


def get_upload_time(pkg_data: dict) -> str:
    """Extract upload_time from package data"""
    info = pkg_data.get("info", {})
    version = info.get("version")
    releases = pkg_data.get("releases", {})
    
    if version and version in releases and releases[version]:
        # Get the first release file (usually the most recent)
        first_release = releases[version][0]
        upload_time = first_release.get("upload_time") or first_release.get("upload_time_iso_8601")
        if upload_time:
            return upload_time
    
    return ""


def get_cache_dir() -> Path:
    """Get cache directory for diskcache (platform-specific)"""
    cache_dir = Path(platformdirs.user_cache_dir("pypipackagestats", "pypipackagestats"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

