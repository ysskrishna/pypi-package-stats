# PyPI Package Stats

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/pypi-package-stats)](https://pypi.org/project/pypi-package-stats/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/pypi-package-stats?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/pypi-package-stats)
[![Documentation](https://img.shields.io/badge/docs-ysskrishna.github.io%2Fpypi--package--stats-blue.svg)](https://ysskrishna.github.io/pypi-package-stats/)


A Python library and optional CLI tool for PyPI package stats and download analytics, built on the official pypistats API. Fetch daily, weekly, monthly, and 180-day downloads, Python version and OS breakdowns, package metadata, with smart disk caching.

![Example Output](https://raw.githubusercontent.com/ysskrishna/pypi-package-stats/main/media/example_output.png)

## Features

- **Package Metadata**: Name, version, description, author, license, home page, and PyPI URL
- **Download Statistics**: Last day, week, month, and 180-day download counts
- **Python Version Breakdown**: Top 5 Python versions with download percentages (last 30 days)
- **Operating System Distribution**: Top 4 operating systems with download percentages (last 30 days)
- **Dual Interface**: Use as a CLI tool or import as a Python library
- **Flexible Output for CLI**: Human-friendly Rich tables or machine-readable JSON
- **Python API**: Clean, type-safe API with structured data models
- **Smart Disk Caching**: Persistent disk cache with configurable TTL (default: 1 hour)
- **Cache Management**: Inspect cache usage or clear cached responses programmatically or via CLI

## Installation

Install the library (no CLI dependencies):

```bash
pip install pypi-package-stats
```

Install with CLI support:

```bash
pip install pypi-package-stats[cli]
```

## Library Usage

```python
from pypipackagestats import get_package_stats

# Get package statistics
stats = get_package_stats("requests")

# Access structured data
print(stats.package_info.name)        # "requests"
print(stats.downloads.last_month)     # 123456789

# Convert to dictionary (for JSON serialization)
data = stats.to_dict()
```

### Advanced Options

```python
from pypipackagestats import get_package_stats, clear_cache, get_cache_info

# Disable caching for fresh data
stats = get_package_stats("requests", no_cache=True)

# Custom cache TTL (5 minutes = 300 seconds)
stats = get_package_stats("django", cache_ttl=300)

# Clear all cached responses
clear_cache()

# Get cache statistics
cache_info = get_cache_info()
print(f"Cache size: {cache_info['size']} entries")
print(f"Cache directory: {cache_info['directory']}")
```

## API Reference

### Functions

| Function | Description |
|----------|-------------|
| `get_package_stats(name, *, no_cache=False, cache_ttl=None)` | Fetch all statistics for a PyPI package. Returns a `PackageStats` object. |
| `clear_cache()` | Clear all cached API responses. |
| `get_cache_info()` | Return cache size and directory information. |


## CLI Usage

> Requires the `cli` extra: `pip install pypi-package-stats[cli]`

| Command | What you get |
|---------|--------------|
| `pypi-package-stats package <name>` | Main view (metadata + downloads) |
| `pypi-package-stats package <name> --json` | Machine-friendly JSON output |
| `pypi-package-stats package <name> --no-cache` | Bypass cache for this request |
| `pypi-package-stats package <name> --cache-ttl <seconds>` | Set custom cache TTL |
| `pypi-package-stats cache-clear` | Remove all cached responses |
| `pypi-package-stats cache-info` | Show cache statistics |
| `pypi-package-stats --help` | Show help message |

**Example:**

```bash
pypi-package-stats package nestedutils --json
```

**Example JSON Output:**

```json
{
  "package": {
    "name": "nestedutils",
    "version": "1.1.7",
    "upload_time": "2026-01-25",
    "description": "The lightweight Python library for safe, simple, dot-notation access to nested dicts and lists. Effortlessly get, set, and delete values deep in your complex JSON, API responses, and config files without verbose error-checking or handling KeyError exceptions.",
    "author": "ysskrishna <sivasaikrishnassk@gmail.com>",
    "license": "MIT",
    "home_page": "https://pypi.org/project/nestedutils/",
    "pypi_url": "https://pypi.org/project/nestedutils/"
  },
  "downloads": {
    "last_day": 1,
    "last_week": 112,
    "last_month": 307,
    "last_180d": 1142
  },
  "python_versions": [
    {
      "version": "null",
      "downloads": 278,
      "percentage": 92.4
    },
    {
      "version": "3.10",
      "downloads": 8,
      "percentage": 2.7
    },
    {
      "version": "3.11",
      "downloads": 4,
      "percentage": 1.3
    },
    {
      "version": "3.12",
      "downloads": 4,
      "percentage": 1.3
    },
    {
      "version": "3.13",
      "downloads": 4,
      "percentage": 1.3
    }
  ],
  "operating_systems": [
    {
      "os": "null",
      "downloads": 278,
      "percentage": 92.4
    },
    {
      "os": "Linux",
      "downloads": 19,
      "percentage": 6.3
    },
    {
      "os": "Darwin",
      "downloads": 4,
      "percentage": 1.3
    }
  ]
}
```

For full CLI documentation, see the [CLI Guide](CLI.md).

## Data Source & Rate Limiting

This tool uses the [pypistats](https://pypistats.org/) API to fetch PyPI package statistics. The API enforces IP-based rate limits (for example, ~5 requests/sec and ~30 requests/min at the time of writing). These limits are set by pypistats.org and may change over time.

The built-in caching system helps minimize API calls and reduce the chance of hitting rate limits. If you encounter rate limit errors, wait a few seconds between requests if making multiple queries.

## Limitations

* Python version and OS breakdowns are limited to the last 30 days
* Data availability depends on the [pypistats](https://pypistats.org/) service
* Data is usually 24-48 hours behind (pypistats limitation)

## Use Cases

* Compare popularity of Python libraries
* Track adoption trends of your own packages
* Generate download statistics for reports or dashboards
* Automate analytics workflows using the library API or CLI JSON output
* Integrate PyPI stats into your Python applications
* Build custom dashboards and monitoring tools


## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/ysskrishna/pypi-package-stats/blob/main/CONTRIBUTING.md) for details.


## Support

If you find this library helpful:

- ⭐ Star the repository
- 🐛 Report issues
- 🔀 Submit pull requests
- 💝 [Sponsor on GitHub](https://github.com/sponsors/ysskrishna)

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](https://github.com/ysskrishna/pypi-package-stats/blob/main/LICENSE) for details.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://ysskrishna.github.io/pypi-package-stats/">Package documentation</a> •
  <a href="https://pypi.org/project/pypi-package-stats/">Package on PyPI</a> •
  <a href="https://github.com/ysskrishna/pypi-package-stats/issues">Report Issues</a> •
  <a href="https://github.com/ysskrishna/pypi-package-stats/blob/main/CHANGELOG.md">Changelog</a> •
  <a href="https://github.com/ysskrishna/pypi-package-stats/releases">Release History</a> •
</p>
