<div align="center">

<br/>

# ◆ snip

**A terminal snippet manager that lives where you work.**

Store, search, and yank code without leaving your shell.

<br/>

[![Python](https://img.shields.io/badge/python-3.10+-7aa2f7?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-73daca?style=flat-square)](LICENSE)
[![Built with Textual](https://img.shields.io/badge/built%20with-Textual-bb9af7?style=flat-square)](https://github.com/Textualize/textual)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS-565f89?style=flat-square)](#install)

<br/>

![snip terminal interface](assets/hero.svg)

<br/>

</div>

---

## The problem

You write a clever one-liner. You close the terminal. Three weeks later you're Googling the same thing again.

**snip** is your personal snippet vault — local, offline, instantly searchable from your terminal. No browser tabs, no account, no sync drama.

---

## Install

### Linux / macOS — one-liner

```bash
git clone https://github.com/phlx0/snip
cd snip
bash install.sh
```

The script creates an isolated virtualenv at `~/.local/share/snip`, installs the package, drops a launcher at `~/.local/bin/snip`, and patches your shell config if that directory isn't already on `$PATH`.

### From PyPI

```bash
pip install snip-tui
```

### From source (dev)

```bash
git clone https://github.com/phlx0/snip
cd snip
make dev          # creates .venv and installs with dev extras
make run          # launch without activating the venv
# or:
source .venv/bin/activate
snip
```

---

## Usage

```bash
snip                              # open the TUI
snip --db ~/Dropbox/snippets.db   # custom db path — easy cloud sync
python -m snip                    # always works, no PATH required
```

---

## Features

| | |
|---|---|
| **Syntax highlighting** | Tokyo Night palette via a custom Pygments style across 20+ languages |
| **Live search** | Filters across title, description, tags, and language as you type |
| **Clipboard copy** | Press `y` to yank a snippet straight to your clipboard |
| **Pin snippets** | Keep your most-used snippets pinned at the top |
| **Tags** | Organise freely — `#docker #devops #git` etc. |
| **Vim-style navigation** | `j`/`k` or arrow keys, `/` to search, `q` to quit |
| **SQLite storage** | Lives in `~/.config/snip/snip.db` — portable, zero-dependency |
| **Fully offline** | No server, no account, your data stays local |

---

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `n` | New snippet |
| `e` | Edit selected snippet |
| `d` | Delete selected snippet |
| `y` | Copy content to clipboard |
| `p` | Toggle pin |
| `/` | Focus search bar |
| `Esc` | Clear search / return to list |
| `↑` `↓` or `j` `k` | Navigate list |
| `q` | Quit |

---

## Project structure

```
snip/
├── assets/
│   └── hero.svg
├── snip/
│   ├── __main__.py          # entry point
│   ├── app.py               # Textual app + demo seeding
│   ├── snip.tcss            # all styling (Tokyo Night palette)
│   ├── models/
│   │   └── snippet.py       # Snippet dataclass
│   ├── storage/
│   │   └── database.py      # SQLite CRUD
│   ├── ui/
│   │   ├── screens/
│   │   │   ├── main_screen.py
│   │   │   └── edit_screen.py
│   │   └── widgets/
│   │       ├── app_header.py
│   │       ├── snippet_list.py
│   │       └── snippet_preview.py
│   └── utils/
│       └── clipboard.py
├── tests/
├── install.sh               # Linux / macOS installer
├── Makefile
└── pyproject.toml
```

---

## Development

```bash
make dev        # create .venv + install with dev extras
make test       # run test suite
make test-cov   # run with coverage report
make run        # launch the app
make clean      # remove build artefacts and .venv
```

---

## Contributing

Bug reports and pull requests are welcome on [GitHub](https://github.com/phlx0/snip/issues).

1. Fork the repo and create a branch: `git checkout -b fix/my-fix`
2. Make your changes and add tests if relevant
3. Run `make test` to make sure everything passes
4. Open a pull request

---

## License

MIT — see [LICENSE](LICENSE).
