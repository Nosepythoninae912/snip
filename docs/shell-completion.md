# Shell completion

snip can tab-complete snippet titles and flags in your shell.

## zsh

Add to `~/.zshrc`:

```bash
eval "$(snip init zsh)"
```

## bash

Add to `~/.bashrc`:

```bash
eval "$(snip init bash)"
```

## What gets completed

- All snippet titles (so `snip por<TAB>` completes to `snip ports`)
- All flags (`--list`, `--add`, `--export`, `run`, etc.)

Restart your shell or `source ~/.zshrc` after adding the line.
