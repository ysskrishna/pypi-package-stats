"""Public API for PyPI Package Stats."""

import threading
import requests
from pypipackagestats.core.client import PyPIClient
from pypipackagestats.core.models import PackageStats
from pypipackagestats.core.processing import process_package_info, process_download_stats, process_category_breakdown
from pypipackagestats.core.exceptions import PackageNotFoundError, APIError, PyPIStatsError

# Thread-local storage for client reuse
_thread_local = threading.local()

def get_package_stats(
    package_name: str,
    *,
    no_cache: bool = False,
    cache_ttl: int = 3600,
) -> PackageStats:
    """
    Get PyPI package statistics (thread-safe).
    
    Args:
        package_name: Package name
        no_cache: Whether to disable caching (default: False)
        cache_ttl: Cache TTL in seconds (default: 3600)
        
    Returns:
        PackageStats: Package statistics
        
    Raises:
        PackageNotFoundError: If package not found
        APIError: If API/network error
        ValueError: If invalid package name
        
    Example:
        >>> stats = get_package_stats("requests")
        >>> print(f"Downloads: {stats.downloads.last_month:,}")
        
    Thread Safety:
        This function is fully thread-safe and can be used safely
        in concurrent environments like ThreadPoolExecutor.
    """
    if not package_name or not package_name.strip():
        raise ValueError("Package name cannot be empty")
    
    package_name = package_name.strip().lower()
    
    # Thread-safe client reuse - each thread gets its own client
    # Client is reused only if cache settings match
    cache_key = f"{no_cache}_{cache_ttl}"
    
    if (not hasattr(_thread_local, 'client') or 
        not hasattr(_thread_local, 'cache_key') or
        _thread_local.cache_key != cache_key):
        
        _thread_local.client = PyPIClient(no_cache=no_cache, cache_ttl=cache_ttl)
        _thread_local.cache_key = cache_key
    
    client = _thread_local.client
    
    try:
        # Fetch all data
        package_data = client.get_package_info(package_name)
        recent_stats = client.get_recent_stats(package_name)
        overall_stats = client.get_overall_stats(package_name)
        python_stats = client.get_python_stats(package_name)
        system_stats = client.get_system_stats(package_name)
        
        # Process data
        return PackageStats(
            package_info=process_package_info(package_data),
            downloads=process_download_stats(recent_stats, overall_stats),
            python_versions=process_category_breakdown(python_stats, 5),
            operating_systems=process_category_breakdown(system_stats, 4),
        )
        
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 404:
            raise PackageNotFoundError(package_name)
        else:
            status_code = e.response.status_code if e.response else None
            raise APIError(f"HTTP {status_code}: {str(e)}", status_code)
    
    except requests.exceptions.RequestException as e:
        raise APIError(f"Network error: {str(e)}")
    
    except Exception as e:
        raise PyPIStatsError(f"Unexpected error: {str(e)}") from e
