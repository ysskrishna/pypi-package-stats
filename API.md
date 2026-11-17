# pypi-package-stats API reference

Install with `pip install pypi-package-stats` and import from `pypipackagestats`. Signatures and descriptions below match the docstrings in `pypipackagestats`.

## `get_package_stats(package_name: str, *, no_cache: bool = False, cache_ttl: Optional[int] = None) -> pypipackagestats.core.models.PackageStats`

Get PyPI package statistics (thread-safe).

**Parameters**

- `package_name`: Package name
- `no_cache`: Whether to disable caching (default: False). If True, sets cache_ttl=0 to disable caching.
- `cache_ttl`: Time-to-live for cache entries in seconds. - Positive integer → cache with that TTL (seconds) - 0 → disable caching completely - None or omitted → use default (3600 seconds)

**Returns**

- `PackageStats`: Package statistics

**Raises**

- `PackageNotFoundError`: If package not found
- `APIError`: If API/network error
- `ValueError`: If invalid package name

**Example**

```python
from pypipackagestats import get_package_stats

stats = get_package_stats("requests")
print(f"Downloads: {stats.downloads.last_month:,}")
```

Thread Safety: This function is fully thread-safe and can be used safely in concurrent environments like ThreadPoolExecutor.

## `clear_cache() -> None`

Clear all cached data.

## `get_cache_info() -> Dict[str, Any]`

Get cache information. Returns a dict with `size` (number of cached entries) and `cache_dir` (path of the on-disk cache).

```python
from pypipackagestats import get_cache_info

info = get_cache_info()
print(info["size"], info["cache_dir"])
```

## `PackageStats(package_info: pypipackagestats.core.models.PackageInfo, downloads: pypipackagestats.core.models.DownloadStats, python_versions: List[pypipackagestats.core.models.CategoryBreakdown], operating_systems: List[pypipackagestats.core.models.CategoryBreakdown]) -> None`

PackageStats(package_info: pypipackagestats.core.models.PackageInfo, downloads: pypipackagestats.core.models.DownloadStats, python_versions: List[pypipackagestats.core.models.CategoryBreakdown], operating_systems: List[pypipackagestats.core.models.CategoryBreakdown])

### `PackageStats.to_dict(self) -> Dict[str, Any]`

Convert to dict for JSON.

## `PyPIStatsError`

Exception class (subclass of `Exception`).

Base exception for PyPI Stats.

## `PackageNotFoundError`

Exception class (subclass of `PyPIStatsError`).

Package not found on PyPI.

## `APIError`

Exception class (subclass of `PyPIStatsError`).

API or network error.


## Data model

`get_package_stats()` returns frozen dataclasses defined in `pypipackagestats/core/models.py`.

### `PackageStats`

| Field | Type |
| --- | --- |
| `package_info` | `PackageInfo` |
| `downloads` | `DownloadStats` |
| `python_versions` | `List[CategoryBreakdown]` |
| `operating_systems` | `List[CategoryBreakdown]` |

### `PackageInfo`

| Field | Type | Default |
| --- | --- | --- |
| `name` | `str` | required |
| `version` | `str` | required |
| `description` | `Optional[str]` | `None` |
| `author` | `Optional[str]` | `None` |
| `license` | `Optional[str]` | `None` |
| `home_page` | `Optional[str]` | `None` |
| `pypi_url` | `Optional[str]` | `None` |
| `upload_time` | `Optional[str]` | `None` |

### `DownloadStats`

| Field | Type | Default |
| --- | --- | --- |
| `last_day` | `int` | `0` |
| `last_week` | `int` | `0` |
| `last_month` | `int` | `0` |
| `last_180d` | `int` | `0` |

### `CategoryBreakdown`

| Field | Type |
| --- | --- |
| `category` | `str` (a Python version such as `3.12`, an OS name such as `Linux`, or `Unknown`) |
| `downloads` | `int` |
| `percentage` | `float` |

### `PackageStats.to_dict()` output

```python
from pypipackagestats import get_package_stats

stats = get_package_stats("requests")
data = stats.to_dict()

data["package"]            # name, version, upload_time (date part only), description, author, license, home_page, pypi_url
data["downloads"]          # last_day, last_week, last_month, last_180d
data["python_versions"]    # list of {"version", "downloads", "percentage"}
data["operating_systems"]  # list of {"os", "downloads", "percentage"}
```
