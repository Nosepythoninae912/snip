# Dotfile sync

snip stores everything in a single SQLite file at `~/.config/snip/snip.db`. You can point it at any path with `--db`, making sync trivial.

## Dropbox / iCloud / Syncthing

```bash
snip --db ~/Dropbox/snip.db
```

To avoid typing `--db` every time, add an alias to your shell config:

```bash
alias snip='snip --db ~/Dropbox/snip.db'
```

## Git-based dotfiles

Export your snippets to JSON and commit that instead of the binary db:

```bash
# export
snip --export > ~/dotfiles/snippets.json

# restore on a new machine
snip --import ~/dotfiles/snippets.json
```

Add a Makefile target or shell alias to keep it in sync:

```bash
alias snip-backup='snip --export > ~/dotfiles/snippets.json'
alias snip-restore='snip --import ~/dotfiles/snippets.json'
```

## Multiple machines

Each machine can run `snip --db /path/to/shared.db` pointing to the same synced file. If two machines edit simultaneously there is no merge — last write wins. For most personal setups this is fine.
