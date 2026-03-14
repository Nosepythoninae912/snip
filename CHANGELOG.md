# Changelog

All notable changes to this project are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) —
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

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

[Unreleased]: https://github.com/phlx0/snip/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/phlx0/snip/releases/tag/v0.1.0
