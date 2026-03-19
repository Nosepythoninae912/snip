# Dotfile sync

snip stores each snippet as a plain Markdown file with frontmatter in `~/.config/snip/snippets/`. This directory is designed to be tracked with git — every snippet is a human-readable, diffable text file.

A SQLite index (`~/.config/snip/snip.db`) is maintained alongside for fast search. It is regenerated automatically from the snippet files on startup and is excluded from git via a `.gitignore` that snip creates automatically.

## Git-native sync

```bash
cd ~/.config/snip
git init
git add snippets/
git commit -m "initial snippets"
git remote add origin git@github.com:you/dotfiles.git
git push -u origin main
```

On another machine:

```bash
git clone git@github.com:you/dotfiles.git ~/.config/snip
snip   # SQLite index is built automatically on first run
```

When you add or edit snippets on one machine:

```bash
cd ~/.config/snip
git add snippets/
git commit -m "add docker cleanup snippet"
git push
```

On the other machine:

```bash
cd ~/.config/snip
git pull
snip   # new snippets are synced into the index on startup
```

## Why this works well

- Each snippet is its own file — adding snippets on two machines produces no merge conflicts
- `git diff` shows exactly what changed in a snippet's title, content, or tags
- `git log` gives you a full history of every snippet
- Files are readable and editable without snip installed

## Custom snippets directory

To use a different location, pass `--db <dir>` and set an alias:

```bash
alias snip='snip --db ~/dotfiles/snippets'
```

## JSON export / import

If you prefer a single-file backup over a git-tracked directory:

```bash
snip --export > ~/dotfiles/snippets.json
snip --import ~/dotfiles/snippets.json
```

## Multiple machines without git

Point all machines at a shared synced directory (Dropbox, Syncthing, etc.):

```bash
alias snip='snip --db ~/Dropbox/snip/snippets'
```

Each machine keeps its own index file locally. Simultaneous edits to the same snippet will produce a file conflict that git or your sync tool can resolve.
