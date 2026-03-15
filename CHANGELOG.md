# Changelog

All notable changes to this project are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) —
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.2.0] — 2026-03-15

### Added
- `snip <query>` — non-interactive snippet lookup: finds a snippet by title, prints content to stdout, and copies it to the clipboard. Exact title match is preferred; falls back to substring match. Multiple matches list candidates.
- `snip --list` — prints all snippet titles one per line, designed for piping into `fzf` or other tools
- `snip --exec <query>` — runs a matched snippet directly as a shell command; exits with the command's return code
- fzf one-liner in README: `snip --list | fzf | xargs snip`

---

## [0.1.0] — 2026-03-14

### Added
- Full TUI built with [Textual](https://github.com/Textualize/textual)
- Snippet list with live search (title, description, tags, language)
- Syntax-highlighted code preview using a custom Tokyo Night Pygments style
- Create / edit / delete snippets via a modal form
- Pin snippets to keep them at the top of the list
- Clipboard copy with `y` (via pyperclip)
- Vim-style navigation (`j`/`k`) and `/` search
- SQLite storage at `~/.config/snip/snip.db`
- Demo snippets seeded on first run
- `install.sh` one-liner installer for Linux / macOS
- `--db` flag for a custom database path (easy Dropbox / iCloud sync)

[Unreleased]: https://github.com/phlx0/snip/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/phlx0/snip/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/phlx0/snip/releases/tag/v0.1.0
