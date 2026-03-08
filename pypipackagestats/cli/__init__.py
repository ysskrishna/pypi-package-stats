import sys


def main():
    try:
        import typer  # noqa: F401
    except ImportError:
        print("Error: CLI dependencies not installed.\n"
              "Install with: pip install pypi-package-stats[cli]",
              file=sys.stderr)
        sys.exit(1)
    from pypipackagestats.cli._app import run_cli
    run_cli()


if __name__ == "__main__":
    main()
