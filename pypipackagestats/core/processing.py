from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
from nestedutils import get_at
from pypipackagestats.core.models import PackageInfo, DownloadStats, CategoryBreakdown
from pypipackagestats.core.constants import TOP_PYTHON_VERSIONS_COUNT

def get_upload_time(pkg_data: dict) -> str:
    """Extract upload_time from package data"""
    version = get_at(pkg_data, "info.version")

    if version:
        # Try to get upload_time from the first release file
        # Use list path to safely handle version strings that might contain special characters
        upload_time = get_at(pkg_data, ["releases", version, 0, "upload_time"])
        if not upload_time:
            upload_time = get_at(pkg_data, ["releases", version, 0, "upload_time_iso_8601"])
        if upload_time:
            return upload_time

    return ""


def _parse_date_safe(date_str: str) -> Optional[date]:
    """Parse ISO date string safely, returning None if invalid."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def process_package_info(data: Dict[str, Any]) -> PackageInfo:
    """Process package metadata."""
    info = get_at(data, "info", default={})

    
    return PackageInfo(
        name=get_at(info, "name", ""),
        version=get_at(info, "version", ""),
        description=get_at(info, "summary"),
        author=get_at(info, "author") or get_at(info, "author_email"),
        license=get_at(info, "license"),
        home_page=(
            get_at(info, "home_page") or 
            get_at(info, "project_url") or 
            get_at(info, ["project_urls", "Homepage"])
        ),
        pypi_url=get_at(info, "package_url"),
        upload_time=get_upload_time(data),
    )

def process_download_stats(recent: Dict[str, Any], overall: List[Dict[str, Any]]) -> DownloadStats:
    """Process download stats."""
    return DownloadStats(
        last_day=get_at(recent, "last_day", default=0),
        last_week=get_at(recent, "last_week", default=0),
        last_month=get_at(recent, "last_month", default=0),
        last_180d=sum(get_at(d, "downloads", default=0) for d in overall),
    )

def process_category_breakdown(data: List[Dict[str, Any]], limit: int = TOP_PYTHON_VERSIONS_COUNT) -> List[CategoryBreakdown]:
    """Process category breakdown."""
    # Last 30 days only
    cutoff = date.today() - timedelta(days=30)
    recent = [d for d in data if (parsed_date := _parse_date_safe(d.get("date", ""))) is not None and parsed_date >= cutoff]
    
    # Aggregate by category
    totals = {}
    for row in recent:
        cat = row.get("category", "unknown")
        downloads = row.get("downloads", 0)
        totals[cat] = totals.get(cat, 0) + downloads
    
    total = sum(totals.values())
    top = sorted(totals.items(), key=lambda x: -x[1])[:limit]
    
    return [
        CategoryBreakdown(
            category="Unknown" if cat == "null" else cat,
            downloads=downloads,
            percentage=round(100 * downloads / total, 1) if total > 0 else 0.0,
        )
        for cat, downloads in top
    ]
