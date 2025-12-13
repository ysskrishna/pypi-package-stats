from rich.console import Console
from rich.table import Table
from rich import box
from typing import Dict, Any
import json
from nestedutils import get_path

from pypipackagestats.utils import (
    get_last_30_days_data,
    aggregate_by_category,
    normalize_os_name,
    humanize_number,
)
from pypipackagestats.constants import (
    TOP_PYTHON_VERSIONS_COUNT,
    TOP_OS_COUNT,
    DATE_ISO_FORMAT_LENGTH,
)

console = Console()


def format_package_info(info: Dict[str, Any], json_output: bool = False) -> str:
    """Format package metadata"""
    upload_time = get_path(info, "upload_time", default="")
    upload_date_str = upload_time[:DATE_ISO_FORMAT_LENGTH] if upload_time else "(unknown)"
    
    if json_output:
        return json.dumps({
            "name": get_path(info, "name", default=""),
            "version": get_path(info, "version", default=""),
            "upload_time": upload_date_str,
            "description": get_path(info, "summary"),
            "author": get_path(info, "author") or get_path(info, "author_email"),
            "license": get_path(info, "license"),
            "home_page": get_path(info, "home_page") or get_path(info, "project_url"),
            "pypi_url": get_path(info, "package_url")
        }, indent=2)
    
    # Rich formatted output
    name = get_path(info, "name", default="")
    version = get_path(info, "version", default="")
    upload_date = upload_date_str
    
    console.print(f"\n[bold cyan]{name} {version}[/bold cyan] [dim]({upload_date})[/dim]")
    console.print(f"Description : {get_path(info, 'summary') or '(none)'}")
    console.print(f"Author      : {get_path(info, 'author') or get_path(info, 'author_email') or '(unknown)'}")
    console.print(f"License     : {get_path(info, 'license') or '(not specified)'}")
    
    home_page = get_path(info, "home_page") or get_path(info, "project_url") or get_path(info, "project_urls.Homepage") or "(none)"
    console.print(f"Home page   : {home_page}")
    console.print(f"PyPI        : {get_path(info, 'package_url') or ''}\n")
    
    return ""


def format_download_stats(recent: Dict, overall: list, json_output: bool = False) -> str:
    """Format download statistics"""
    total_180d = sum(get_path(d, "downloads", default=0) for d in overall)
    
    stats = {
        "last_day": get_path(recent, "last_day", default=0),
        "last_week": get_path(recent, "last_week", default=0),
        "last_month": get_path(recent, "last_month", default=0),
        "last_180d": total_180d
    }
    
    if json_output:
        return json.dumps({"downloads": stats}, indent=2)
    
    # Rich table
    table = Table(title="Downloads (excluding mirrors)", box=box.ROUNDED)
    table.add_column("Period", style="cyan")
    table.add_column("Downloads", style="green", justify="right")
    
    table.add_row("Last day", humanize_number(stats["last_day"]))
    table.add_row("Last week", humanize_number(stats["last_week"]))
    table.add_row("Last month", humanize_number(stats["last_month"]))
    table.add_row("Last 180d", humanize_number(stats["last_180d"]))
    
    console.print(table)
    console.print()
    return ""


def format_python_versions(py_data: list, json_output: bool = False) -> str:
    """Format Python version breakdown"""
    last30 = get_last_30_days_data(py_data)
    totals = aggregate_by_category(last30)
    total_downloads = sum(totals.values())
    top_py = sorted(totals.items(), key=lambda x: -x[1])[:TOP_PYTHON_VERSIONS_COUNT]
    
    if json_output:
        result = {
            "python_versions": [
                {
                    "version": cat or "null",
                    "percentage": round(100 * v / total_downloads, 1),
                    "downloads": v
                }
                for cat, v in top_py
            ]
        }
        return json.dumps(result, indent=2)
    
    # Rich table
    table = Table(title="Top Python versions (last 30 days)", box=box.ROUNDED)
    table.add_column("Version", style="cyan")
    table.add_column("%", style="yellow", justify="right")
    table.add_column("Downloads", style="green", justify="right")
    
    for cat, v in top_py:
        pct = 100 * v / total_downloads
        table.add_row(
            cat or "null",
            f"{pct:.1f}%",
            humanize_number(v)
        )
    
    console.print(table)
    console.print()
    return ""


def format_os_distribution(os_data: list, json_output: bool = False) -> str:
    """Format OS distribution"""
    last30 = get_last_30_days_data(os_data)
    totals = aggregate_by_category(last30)
    total_downloads = sum(totals.values())
    top_os = sorted(totals.items(), key=lambda x: -x[1])[:TOP_OS_COUNT]
    
    if json_output:
        result = {
            "operating_systems": [
                {
                    "os": normalize_os_name(cat),
                    "percentage": round(100 * v / total_downloads, 1),
                    "downloads": v
                }
                for cat, v in top_os
            ]
        }
        return json.dumps(result, indent=2)
    
    # Rich table
    table = Table(title="Top operating systems (last 30 days)", box=box.ROUNDED)
    table.add_column("OS", style="cyan")
    table.add_column("%", style="yellow", justify="right")
    table.add_column("Downloads", style="green", justify="right")
    
    for cat, v in top_os:
        pct = 100 * v / total_downloads
        table.add_row(
            normalize_os_name(cat),
            f"{pct:.1f}%",
            humanize_number(v)
        )
    
    console.print(table)
    return ""

