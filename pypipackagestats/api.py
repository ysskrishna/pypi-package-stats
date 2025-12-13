import requests
import diskcache
from pathlib import Path
from typing import Optional
from pypipackagestats.utils import get_cache_dir
from pypipackagestats.constants import DEFAULT_CACHE_TTL


class PyPIClient:
    PYPI_API = "https://pypi.org/pypi/{pkg}/json"
    STATS_API = "https://pypistats.org/api/packages/{pkg}/"
    
    def __init__(self, cache_ttl: Optional[int] = DEFAULT_CACHE_TTL):
        """
        Initialize PyPI client with persistent disk cache.
        
        Args:
            cache_ttl: Time-to-live for cache entries in seconds.
                      - Positive integer → cache with that TTL (seconds)
                      - 0 → disable caching completely
                      - None or omitted → use default (3600 seconds)
        """
        if cache_ttl == 0:
            # Disable caching
            self.cache = None
            self.cache_ttl = 0
        else:
            # Enable caching with provided TTL or default
            self.cache_ttl = cache_ttl or DEFAULT_CACHE_TTL
            cache_dir = get_cache_dir() / "api_cache"
            self.cache = diskcache.Cache(cache_dir)
    
    def _cached_get(self, url: str) -> dict:
        """
        Get URL with persistent disk caching.
        
        Cache keys are based on URL, and entries expire after cache_ttl seconds.
        """
        if self.cache is None:
            # No cache - direct API call
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        
        # Check cache first
        cache_key = f"url:{url}"
        
        # Try to get from cache
        cached_data = self.cache.get(cache_key, default=None, expire_time=self.cache_ttl)
        
        if cached_data is not None:
            return cached_data
        
        # Cache miss - fetch from API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Store in cache
        self.cache.set(cache_key, data, expire=self.cache_ttl)
        
        return data
    
    def get_package_info(self, package: str) -> dict:
        """Fetch package metadata from PyPI"""
        url = self.PYPI_API.format(pkg=package.lower())
        return self._cached_get(url)
    
    def get_recent_stats(self, package: str) -> dict:
        """Get recent download stats"""
        url = self.STATS_API.format(pkg=package.lower()) + "recent"
        return self._cached_get(url)["data"]
    
    def get_overall_stats(self, package: str) -> list:
        """Get overall stats (180 days)"""
        url = self.STATS_API.format(pkg=package.lower()) + "overall?mirrors=false"
        return self._cached_get(url)["data"]
    
    def get_python_minor_stats(self, package: str) -> list:
        """Get Python version breakdown"""
        url = self.STATS_API.format(pkg=package.lower()) + "python_minor"
        return self._cached_get(url)["data"]
    
    def get_system_stats(self, package: str) -> list:
        """Get OS breakdown"""
        url = self.STATS_API.format(pkg=package.lower()) + "system"
        return self._cached_get(url)["data"]
    
    def clear_cache(self):
        """Clear all cached data"""
        if self.cache is not None:
            self.cache.clear()
    
    def get_cache_size(self) -> int:
        """Get number of items in cache"""
        if self.cache is not None:
            return len(self.cache)
        return 0

