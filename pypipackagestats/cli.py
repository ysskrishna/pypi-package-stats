import typer
import requests
import json as json_lib
from typing import Optional
from rich.console import Console

from pypipackagestats.api import PyPIClient
from pypipackagestats.formatters import (
    format_package_info,
    format_download_stats,
    format_python_versions,
    format_os_distribution,
)
from pypipackagestats.utils import get_last_30_days_data, aggregate_by_category, normalize_os_name, get_cache_dir
from pypipackagestats.constants import (
    DEFAULT_CACHE_TTL,
    TOP_PYTHON_VERSIONS_COUNT,
    TOP_OS_COUNT,
    DATE_ISO_FORMAT_LENGTH,
)

app = typer.Typer(help="Get comprehensive PyPI package information")
console = Console()


@app.command()
def main(
    package: str = typer.Argument(..., help="Package name to query"),
    json: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
    cache_ttl: Optional[int] = typer.Option(
        None,
        "--cache-ttl",
        help=f"Cache TTL in seconds (default: {DEFAULT_CACHE_TTL} seconds). Use 0 to disable cache."
    ),
    no_cache: bool = typer.Option(
        False,
        "--no-cache",
        help="Disable caching entirely (bypasses cache for this run)"
    ),
):
    """
    Display comprehensive information about a PyPI package.
    
    Shows package metadata, download statistics, Python version breakdown,
    and OS distribution. Use --json for machine-readable output.
    
    Caching:
    - Default cache TTL: 1 hour (3600 seconds)
    - Cache persists between CLI runs (stored on disk)
    - Use --cache-ttl to set custom TTL
    - Use --no-cache to bypass cache for this run
    """
    # Determine cache settings
    use_cache = not no_cache
    ttl = cache_ttl if cache_ttl is not None else DEFAULT_CACHE_TTL
    
    # If cache_ttl is 0, disable cache
    if cache_ttl == 0:
        use_cache = False
    
    client = PyPIClient(cache_ttl=ttl, use_cache=use_cache)
    
    try:
        # Fetch all data
        pkg_data = client.get_package_info(package)
        package_info = pkg_data["info"]
        
        recent_stats = client.get_recent_stats(package)
        overall_stats = client.get_overall_stats(package)
        py_stats = client.get_python_minor_stats(package)
        os_stats = client.get_system_stats(package)
        
        if json:
            # JSON output mode
            total_180d = sum(d["downloads"] for d in overall_stats)
            py_last30 = get_last_30_days_data(py_stats)
            os_last30 = get_last_30_days_data(os_stats)
            
            py_totals = aggregate_by_category(py_last30)
            os_totals = aggregate_by_category(os_last30)
            total_py = sum(py_totals.values())
            total_os = sum(os_totals.values())
            
            top_py = sorted(py_totals.items(), key=lambda x: -x[1])[:TOP_PYTHON_VERSIONS_COUNT]
            top_os = sorted(os_totals.items(), key=lambda x: -x[1])[:TOP_OS_COUNT]
            
            output = {
                "package": {
                    "name": package_info["name"],
                    "version": package_info["version"],
                    "upload_time": package_info["upload_time"][:DATE_ISO_FORMAT_LENGTH],
                    "description": package_info.get("summary"),
                    "author": package_info.get("author") or package_info.get("author_email"),
                    "license": package_info.get("license"),
                    "home_page": package_info.get("home_page") or package_info.get("project_url"),
                    "pypi_url": package_info.get("package_url")
                },
                "downloads": {
                    "last_day": recent_stats["last_day"],
                    "last_week": recent_stats["last_week"],
                    "last_month": recent_stats["last_month"],
                    "last_180d": total_180d
                },
                "python_versions": [
                    {
                        "version": cat or "null",
                        "percentage": round(100 * v / total_py, 1),
                        "downloads": v
                    }
                    for cat, v in top_py
                ],
                "operating_systems": [
                    {
                        "os": normalize_os_name(cat),
                        "percentage": round(100 * v / total_os, 1),
                        "downloads": v
                    }
                    for cat, v in top_os
                ]
            }
            
            console.print(json_lib.dumps(output, indent=2))
        else:
            # Formatted output mode
            format_package_info(package_info, json_output=False)
            format_download_stats(recent_stats, overall_stats, json_output=False)
            format_python_versions(py_stats, json_output=False)
            format_os_distribution(os_stats, json_output=False)
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            console.print(f"[red]Error:[/red] Package '{package}' not found on PyPI")
            raise typer.Exit(1)
        else:
            console.print(f"[red]Error:[/red] HTTP {e.response.status_code}: {e}")
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def clear_cache():
    """Clear all cached data"""
    client = PyPIClient()
    client.clear_cache()
    console.print("[green]Cache cleared successfully[/green]")


@app.command()
def cache_info():
    """Show cache information"""
    client = PyPIClient()
    cache_dir = get_cache_dir()
    cache_size = client.get_cache_size()
    
    console.print(f"[cyan]Cache directory:[/cyan] {cache_dir / 'api_cache'}")
    console.print(f"[cyan]Cache entries:[/cyan] {cache_size}")
    console.print(f"[cyan]Cache TTL:[/cyan] {client.cache_ttl} seconds ({client.cache_ttl / 3600:.1f} hours)")


if __name__ == "__main__":
    app()

