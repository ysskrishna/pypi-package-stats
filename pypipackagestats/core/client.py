import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
from typing import Dict, Any
from nestedutils import get_at
from pypipackagestats.core.cache import cached_get

class PyPIClient:
    """Thread-safe PyPI API client."""
    
    def __init__(self, use_cache: bool = True, cache_ttl: int = 3600):
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        self._local = threading.local()
    
    def _get_session(self) -> requests.Session:
        """Get thread-local session."""
        if not hasattr(self._local, 'session'):
            session = requests.Session()
            retry = Retry(
                total=3, 
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=1,
                respect_retry_after_header=True
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)
            session.mount("http://", adapter)
            self._local.session = session
        return self._local.session
    
    def _get(self, url: str) -> Dict[str, Any]:
        """Thread-safe GET with caching."""
        return cached_get(url, self._get_session(), self.cache_ttl, self.use_cache)
    
    def get_package_info(self, package: str) -> Dict[str, Any]:
        """Get package metadata."""
        return self._get(f"https://pypi.org/pypi/{package.lower()}/json")
    
    def get_recent_stats(self, package: str) -> Dict[str, Any]:
        """Get recent download stats."""
        url = f"https://pypistats.org/api/packages/{package.lower()}/recent"
        return get_at(self._get(url), "data", default={})
    
    def get_overall_stats(self, package: str) -> list:
        """Get overall stats."""
        url = f"https://pypistats.org/api/packages/{package.lower()}/overall?mirrors=false"
        return get_at(self._get(url), "data", default=[])
    
    def get_python_stats(self, package: str) -> list:
        """Get Python version stats."""
        url = f"https://pypistats.org/api/packages/{package.lower()}/python_minor"
        return get_at(self._get(url), "data", default=[])
    
    def get_system_stats(self, package: str) -> list:
        """Get OS stats."""
        url = f"https://pypistats.org/api/packages/{package.lower()}/system"
        return get_at(self._get(url), "data", default=[])

