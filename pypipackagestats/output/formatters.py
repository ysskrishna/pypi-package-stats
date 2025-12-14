from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box
from typing import Dict, Any
from pypipackagestats.core.metadata import get_project_metadata
from pypipackagestats.output.utils import normalize_os_name

from pypipackagestats.output.utils import humanize_number

console = Console()


def format_package_info(data: Dict[str, Any]) -> None:
    pkg = data["package"]

    console.print(f"\n[bold cyan]{pkg['name']}[/bold cyan]")
    console.print(f"{pkg['description'] or '(none)'}")
    console.print(f"Version     : {pkg['version']}")
    console.print(f"Upload time : {pkg['upload_time']}")
    console.print(f"Author      : {pkg['author'] or '(unknown)'}")
    console.print(f"License     : {pkg['license'] or '(not specified)'}")
    console.print(f"Home page   : {pkg['home_page'] or '(none)'}")
    console.print(f"PyPI        : {pkg['pypi_url']}\n")


def format_download_stats(data: Dict[str, Any]) -> None:
    dl = data["downloads"]

    table = Table(title="Downloads (excluding mirrors)", box=box.ROUNDED)
    table.add_column("Period", style="cyan")
    table.add_column("Downloads", style="green", justify="right")

    table.add_row("Last day", humanize_number(dl["last_day"]))
    table.add_row("Last week", humanize_number(dl["last_week"]))
    table.add_row("Last month", humanize_number(dl["last_month"]))
    table.add_row("Last 180 days", humanize_number(dl["last_180d"]))

    console.print(table)
    console.print()


def format_python_versions(data: Dict[str, Any]) -> None:
    versions = data["python_versions"]

    if not versions:
        console.print("[yellow]No Python version data available for last 30 days.[/yellow]\n")
        return

    table = Table(title="Top Python versions (last 30 days)", box=box.ROUNDED)
    table.add_column("Version", style="cyan")
    table.add_column("Share", style="yellow", justify="right")
    table.add_column("Downloads", style="green", justify="right")

    for item in versions:
        version = item["version"] if item["version"] != "null" else "Unknown"
        table.add_row(
            version,
            f"{item['percentage']:.1f}%",
            humanize_number(item["downloads"])
        )

    console.print(table)
    console.print()


def format_os_distribution(data: Dict[str, Any]) -> None:
    systems = data["operating_systems"]

    if not systems:
        console.print("[yellow]No OS distribution data available for last 30 days.[/yellow]")
        return

    table = Table(title="Top operating systems (last 30 days)", box=box.ROUNDED)
    table.add_column("OS", style="cyan")
    table.add_column("Share", style="yellow", justify="right")
    table.add_column("Downloads", style="green", justify="right")

    for item in systems:
        table.add_row(
            normalize_os_name(item["os"]),
            f"{item['percentage']:.1f}%",
            humanize_number(item["downloads"])
        )

    console.print(table)


def print_project_banner():
    banner_text = Text()
    project_metadata = get_project_metadata()
    
    # ASCII art for "PYPI STATS"
    banner_text.append("\n  _____       _____ _____   _____           _                       _____ _        _       ", style="bold blue")
    banner_text.append("\n |  __ \\     |  __ \\_   _| |  __ \\         | |                     / ____| |      | |      ", style="bold blue")
    banner_text.append("\n | |__) |   _| |__) || |   | |__) |_ _  ___| | ____ _  __ _  ___  | (___ | |_ __ _| |_ ___ ", style="bold blue")
    banner_text.append("\n |  ___/ | | |  ___/ | |   |  ___/ _` |/ __| |/ / _` |/ _` |/ _ \\  \\___ \\| __/ _` | __/ __|", style="bold blue")
    banner_text.append("\n | |   | |_| | |    _| |_  | |  | (_| | (__|   < (_| | (_| |  __/  ____) | || (_| | |_\\__ \\", style="bold blue")
    banner_text.append("\n |_|    \\__, |_|   |_____| |_|   \\__,_|\\___|_|\\_\\__,_|\\__, |\\___| |_____/ \\__\\__,_|\\__|___/", style="bold blue")
    banner_text.append("\n         __/ |                                         __/ |                               ", style="bold blue")
    banner_text.append("\n        |___/                                         |___/                                \n", style="bold blue")
    
    banner_text.append(f"Version : {project_metadata.version}\n", style="bold blue")
    banner_text.append(f"Author  : {project_metadata.author} ({project_metadata.author_url})\n", style="magenta")
    banner_text.append(f"Repo    : {project_metadata.repository_url}\n", style="green")
    
    console.print(Panel(banner_text, expand=False, border_style="blue", title="Welcome", title_align="left"))
