import threading
from pathlib import Path
from typing import Dict, Any, Optional
import platformdirs
import diskcache

# Global thread-safe cache
_cache_lock = threading.RLock()
_cache_instance: Optional[diskcache.Cache] = None

def get_cache_dir() -> Path:
    """Get cache directory."""
    cache_dir = Path(platformdirs.user_cache_dir("pypipackagestats"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def get_cache() -> diskcache.Cache:
    """Get thread-safe shared cache instance."""
    global _cache_instance
    if _cache_instance is None:
        with _cache_lock:
            if _cache_instance is None:
                _cache_instance = diskcache.Cache(get_cache_dir() / "cache")
    return _cache_instance

def cached_get(url: str, session, cache_ttl: int, use_cache: bool) -> Dict[str, Any]:
    """Thread-safe cached GET request."""
    if not use_cache:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    
    cache = get_cache()
    
    # Thread-safe cache read
    with _cache_lock:
        cached_data = cache.get(url, default=None)
    
    if cached_data is not None:
        return cached_data
    
    # Fetch from API
    response = session.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Thread-safe cache write
    with _cache_lock:
        cache.set(url, data, expire=cache_ttl)
    
    return data

def clear_cache() -> None:
    """Clear all cached data (thread-safe)."""
    with _cache_lock:
        get_cache().clear()

def get_cache_info() -> Dict[str, Any]:
    """Get cache information (thread-safe)."""
    cache = get_cache()
    with _cache_lock:
        size = len(cache)
    
    return {
        "size": size,
        "cache_dir": str(get_cache_dir() / "cache"),
    }
