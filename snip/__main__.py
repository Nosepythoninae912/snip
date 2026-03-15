import json
import os
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


def _lang_from_ext(path: Path) -> str:
    mapping = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".sh": "bash", ".bash": "bash", ".zsh": "bash",
        ".go": "go", ".rs": "rust", ".c": "c", ".cpp": "cpp",
        ".java": "java", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
        ".toml": "toml", ".sql": "sql", ".html": "html", ".css": "css",
        ".md": "markdown", ".rb": "ruby", ".php": "php",
        ".dockerfile": "dockerfile", ".ps1": "powershell",
    }
    name = path.name.lower()
    if name == "dockerfile":
        return "dockerfile"
    return mapping.get(path.suffix.lower(), "text")


def _run_add(file_path: str, db_path: Path) -> None:
    from snip.models.snippet import Snippet
    from snip.storage.database import Database

    path = Path(file_path)
    if not path.exists():
        print(f"snip: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text()
    title = path.stem
    language = _lang_from_ext(path)

    db = Database(db_path)
    snippet = db.create(Snippet(title=title, content=content, language=language))
    print(f"Saved '{snippet.title}' (id {snippet.id}, language: {language})")


def _run_export(db_path: Path) -> None:
    from snip.storage.database import Database

    db = Database(db_path)
    data = [
        {
            "title": s.title,
            "content": s.content,
            "language": s.language,
            "description": s.description,
            "tags": s.tags,
            "pinned": s.pinned,
        }
        for s in db.get_all()
    ]
    print(json.dumps(data, indent=2))


def _run_import(file_path: str, db_path: Path) -> None:
    from snip.models.snippet import Snippet
    from snip.storage.database import Database

    if file_path == "-":
        raw = sys.stdin.read()
    else:
        p = Path(file_path)
        if not p.exists():
            print(f"snip: file not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        raw = p.read_text()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"snip: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    db = Database(db_path)
    for i, item in enumerate(data):
        if "title" not in item or "content" not in item:
            print(f"snip: skipping entry {i} — missing title or content", file=sys.stderr)
            continue
        db.create(Snippet(
            title=item["title"],
            content=item["content"],
            language=item.get("language", "text"),
            description=item.get("description", ""),
            tags=item.get("tags", []),
            pinned=item.get("pinned", False),
        ))
        print(f"  imported '{item['title']}'")

    print(f"\nDone. {len(data)} snippet(s) imported.")


def _read_history() -> list[str]:
    """Read shell history, returning deduplicated commands, most recent first."""
    shell = os.environ.get("SHELL", "")
    candidates = []

    if "zsh" in shell:
        candidates.append(Path.home() / ".zsh_history")
    candidates.append(Path.home() / ".bash_history")

    for hist_file in candidates:
        if not hist_file.exists():
            continue
        lines = hist_file.read_text(errors="replace").splitlines()
        cmds = []
        for line in lines:
            # zsh extended history format: `: timestamp:elapsed;command`
            if line.startswith(":") and ";" in line:
                line = line.split(";", 1)[1]
            line = line.strip()
            if line and not line.startswith("#"):
                cmds.append(line)
        # deduplicate preserving last occurrence (most recent)
        seen: set[str] = set()
        deduped = []
        for cmd in reversed(cmds):
            if cmd not in seen:
                seen.add(cmd)
                deduped.append(cmd)
        return deduped  # most recent first

    return []


def _run_from_history(db_path: Path) -> None:
    from snip.models.snippet import Snippet
    from snip.storage.database import Database

    history = _read_history()
    if not history:
        print("snip: no shell history found", file=sys.stderr)
        sys.exit(1)

    # Prefer fzf for selection
    if subprocess.run(["which", "fzf"], capture_output=True).returncode == 0:
        result = subprocess.run(
            ["fzf", "--prompt=pick a command > ", "--height=40%", "--reverse"],
            input="\n".join(history),
            text=True,
            capture_output=True,
        )
        if result.returncode != 0 or not result.stdout.strip():
            print("snip: nothing selected", file=sys.stderr)
            sys.exit(0)
        command = result.stdout.strip()
    else:
        # Fallback: numbered list
        preview = history[:50]
        for i, cmd in enumerate(preview, 1):
            print(f"  {i:>3}.  {cmd}")
        print()
        try:
            choice = input("Pick a number (or q to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if choice.lower() == "q":
            sys.exit(0)
        try:
            command = preview[int(choice) - 1]
        except (ValueError, IndexError):
            print("snip: invalid selection", file=sys.stderr)
            sys.exit(1)

    print(f"\n  command: {command}")
    try:
        title = input("  title (leave blank to use command): ").strip()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)
    if not title:
        title = command[:60]

    db = Database(db_path)
    snippet = db.create(Snippet(title=title, content=command, language="bash"))
    print(f"\nSaved '{snippet.title}' (id {snippet.id})")


def main() -> None:
    from snip.app import _DEFAULT_DB

    db_path: Path = _DEFAULT_DB
    args = sys.argv[1:]

    # Strip --db <path> from args
    if len(args) >= 2 and args[0] == "--db":
        db_path = Path(args[1])
        args = args[2:]

    try:
        if not args:
            _run_tui(db_path)
        elif args[0] == "--list":
            _run_list(db_path)
        elif args[0] in ("--exec", "run") and len(args) >= 2:
            _run_exec(" ".join(args[1:]), db_path)
        elif args[0] == "--add" and len(args) >= 2:
            _run_add(args[1], db_path)
        elif args[0] == "--export":
            _run_export(db_path)
        elif args[0] == "--import" and len(args) >= 2:
            _run_import(args[1], db_path)
        elif args[0] == "--from-history":
            _run_from_history(db_path)
        else:
            _run_copy(" ".join(args), db_path)
    except ImportError as e:
        print(f"snip: missing dependency — {e}", file=sys.stderr)
        print("Run: pip install textual pyperclip", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"snip: failed to start — {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
