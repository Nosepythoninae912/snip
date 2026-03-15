import subprocess
import sys
from pathlib import Path


def _run_tui(db_path: Path) -> None:
    from snip.app import SnipApp
    SnipApp(db_path=db_path).run()


def _run_list(db_path: Path) -> None:
    from snip.storage.database import Database

    db = Database(db_path)
    for s in db.get_all():
        print(s.title)


def _resolve(query: str, db_path: Path):
    from snip.storage.database import Database

    db = Database(db_path)
    snippets = db.get_all()
    q = query.lower()
    exact = [s for s in snippets if s.title.lower() == q]
    matches = exact or [s for s in snippets if q in s.title.lower()]

    if not matches:
        print(f"snip: no snippet matching '{query}'", file=sys.stderr)
        sys.exit(1)

    if len(matches) > 1:
        print(f"snip: {len(matches)} snippets match '{query}' — be more specific:", file=sys.stderr)
        for s in matches:
            print(f"  • {s.title}", file=sys.stderr)
        sys.exit(1)

    return matches[0]


def _run_copy(query: str, db_path: Path) -> None:
    from snip.utils.clipboard import copy_to_clipboard

    snippet = _resolve(query, db_path)
    print(snippet.content)
    if copy_to_clipboard(snippet.content):
        print(f"Copied '{snippet.title}' to clipboard.", file=sys.stderr)


def _run_exec(query: str, db_path: Path) -> None:
    snippet = _resolve(query, db_path)
    result = subprocess.run(snippet.content, shell=True)
    sys.exit(result.returncode)


def main() -> None:
    from snip.app import _DEFAULT_DB

    db_path: Path = _DEFAULT_DB
    args = sys.argv[1:]

    # Strip --db <path> from args
    if len(args) >= 2 and args[0] == "--db":
        db_path = Path(args[1])
        args = args[2:]

    try:
        if args and args[0] == "--list":
            _run_list(db_path)
        elif len(args) >= 2 and args[0] == "--exec":
            query = " ".join(args[1:])
            _run_exec(query, db_path)
        elif args:
            query = " ".join(args)
            _run_copy(query, db_path)
        else:
            _run_tui(db_path)
    except ImportError as e:
        print(f"snip: missing dependency — {e}", file=sys.stderr)
        print("Run: pip install textual pyperclip", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"snip: failed to start — {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
