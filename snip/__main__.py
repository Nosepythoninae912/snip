import sys
from pathlib import Path


def main() -> None:
    db_path: Path | None = None

    # Allow `snip --db /path/to/custom.db` for power users / testing
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--db":
        db_path = Path(args[1])

    try:
        from snip.app import SnipApp, _DEFAULT_DB

        app = SnipApp(db_path=db_path or _DEFAULT_DB)
        app.run()
    except ImportError as e:
        print(f"snip: missing dependency — {e}", file=sys.stderr)
        print("Run: pip install textual pyperclip", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"snip: failed to start — {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
