# Changelog

All notable changes to this project are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) —
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Fixed
- Demo snippets no longer reappear after deleting all snippets; seeding now only runs on a genuine first install (when the database file does not yet exist)
- Arrow-key navigation in the new/edit snippet form no longer gets stuck in the language selector
- Navigating down from the title field opens the language dropdown automatically; navigating up from description also opens it
- At the top of the language list, pressing up closes the dropdown and moves focus to the title field; at the bottom, pressing down closes it and moves to description
- Arrow keys in the code field navigate lines normally; at the first line pressing up moves to tags, at the last line pressing down moves to the cancel/save buttons
- `up`/`down` navigation no longer wraps around (no more carousel behaviour)
- Pressing `Enter` in any text input (title, description, tags) advances focus to the next field

### Added
- `ctrl+s` saves the snippet from anywhere in the form, including from inside the code editor

---

## [0.4.0] — 2026-03-15

### Added
- `snip --delete <query>` — delete a snippet by title without opening the TUI
- `snip --json <query>` — output full snippet metadata as JSON for scripting
- `snip --list <tag>` — filter listed titles by tag
- `snip --version` / `-v` — print version string
- `snip -q` / `--quiet` — suppress informational stderr output for clean scripting
- `snip init zsh` / `snip init bash` — print shell completion scripts; activate with `eval "$(snip init zsh)"`; tab-completes snippet titles and all flags

---

## [0.3.0] — 2026-03-15

### Added
- `snip run <query>` — cleaner alias for running a snippet as a shell command
- `snip --add <file>` — save any file as a snippet; language auto-detected from extension
- `snip --export` — dump all snippets to JSON on stdout (pipe to a file for dotfile backups)
- `snip --import <file>` — bulk-import snippets from a JSON file (`-` to read from stdin)
- `snip --from-history` — interactively pick a command from shell history (bash/zsh) and save it as a snippet; uses `fzf` if available, falls back to a numbered list

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
