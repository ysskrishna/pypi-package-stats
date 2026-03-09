from datetime import datetime
from pypipackagestats.core.constants import DATE_ISO_FORMAT_LENGTH


def humanize_number(num: int) -> str:
    """Convert large numbers to human-readable format (K, M, B)"""
    for unit in ['', 'K', 'M', 'B']:
        if abs(num) < 1000:
            return f"{num:,.1f}{unit}".rstrip('0').rstrip('.')
        num /= 1000
    return f"{num:,.1f}T"


def normalize_os_name(os_name: str) -> str:
    """Normalize OS names for display"""
    if not os_name or (os_name and os_name.lower() == "null"):
        return "Unknown"
    mapping = {
        "darwin": "macOS",
        "windows": "Windows",
        "linux": "Linux"
    }
    return mapping.get(os_name.lower(), os_name.title())


def humanize_date(date_str: str) -> str:
    """Convert ISO date string (YYYY-MM-DD) to human-readable format"""
    if not date_str:
        return date_str

    try:
        # Parse ISO date format (YYYY-MM-DD)
        dt = datetime.strptime(date_str[:DATE_ISO_FORMAT_LENGTH], "%Y-%m-%d")
        # Format as "Month Day, Year" (e.g., "December 7, 2025")
        return dt.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        # If parsing fails, return the original string
        return date_str


def extract_repo_name(repository_url: str) -> str:
    """Extract repo name from URL (e.g., "https://github.com/owner/repo.git" -> "owner/repo").

    Args:
        repository_url: The full repository URL

    Returns:
        The extracted repo name in format "owner/repo", or empty string if extraction fails
    """
    if not repository_url:
        return ""

    # Remove .git suffix if present
    repo_name = repository_url[:-4] if repository_url.endswith('.git') else repository_url

    # Extract owner/repo from URL
    if 'github.com/' in repo_name:
        repo_name = repo_name.split('github.com/')[-1]
    elif 'gitlab.com/' in repo_name:
        repo_name = repo_name.split('gitlab.com/')[-1]
    elif 'bitbucket.org/' in repo_name:
        repo_name = repo_name.split('bitbucket.org/')[-1]

    return repo_name
