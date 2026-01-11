from pathlib import Path
from typing import Dict, Any
import platformdirs
import diskcache

def get_cache_dir() -> Path:
    """Get cache directory."""
    cache_dir = Path(platformdirs.user_cache_dir("pypipackagestats"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def get_cache() -> diskcache.Cache:
    """Get cache instance - diskcache handles thread safety."""
    cache_dir = get_cache_dir() / "api_cache"
    return diskcache.Cache(cache_dir)

def clear_cache() -> None:
    """Clear all cached data."""
    get_cache().clear()

def get_cache_info() -> Dict[str, Any]:
    """Get cache information."""
    cache = get_cache()
    return {
        "size": len(cache),
        "cache_dir": str(get_cache_dir() / "api_cache"),
    }
