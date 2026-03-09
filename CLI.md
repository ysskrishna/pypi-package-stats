# CLI Guide

> Requires the `cli` extra: `pip install pypi-package-stats[cli]`

## Installation

```bash
pip install pypi-package-stats[cli]
```

## Example Output

![Example Output](https://raw.githubusercontent.com/ysskrishna/pypi-package-stats/main/media/example_output.png)

## Command Reference

### `package` — Fetch package statistics

```bash
pypi-package-stats package <name> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--json`, `-j` | Output as machine-readable JSON |
| `--no-cache` | Bypass cache for this request |
| `--cache-ttl <seconds>` | Set custom cache TTL (default: 3600) |

**Examples:**

```bash
# Human-friendly Rich table output
pypi-package-stats package requests

# Machine-readable JSON output
pypi-package-stats package requests --json

# Fresh data (bypass cache)
pypi-package-stats package django --no-cache

# Custom cache TTL (5 minutes)
pypi-package-stats package flask --cache-ttl 300
```

### `cache-clear` — Clear cached responses

```bash
pypi-package-stats cache-clear
```

### `cache-info` — Show cache statistics

```bash
pypi-package-stats cache-info
```

### `--help` — Show help

```bash
pypi-package-stats --help
```

## Example JSON Output

```bash
pypi-package-stats package nestedutils --json
```

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

## Troubleshooting

### CLI dependencies not installed

If you see:

```
Error: CLI dependencies not installed.
Install with: pip install pypi-package-stats[cli]
```

Install the CLI extras:

```bash
pip install pypi-package-stats[cli]
```

### Rate limit errors

The pypistats.org API enforces IP-based rate limits. The built-in caching helps minimize API calls. If you still hit rate limits:

- Wait a few seconds between requests
- Use the default cache (avoid `--no-cache` unless necessary)
- Increase the cache TTL with `--cache-ttl`

### Package not found

Ensure the package name matches the exact PyPI package name. Package names are case-insensitive but must exist on PyPI.
