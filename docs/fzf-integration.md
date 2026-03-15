# fzf integration

[fzf](https://github.com/junegunn/fzf) pairs naturally with snip. Here are some useful combos.

## Fuzzy-pick and copy

```bash
snip --list | fzf | xargs snip
```

Opens a fuzzy finder over all your snippet titles. Select one and it gets copied to your clipboard.

## Fuzzy-pick and run

```bash
snip --list | fzf | xargs snip run
```

Same as above but runs the snippet as a shell command instead of copying it.

## Filter by tag, then pick

```bash
snip --list docker | fzf | xargs snip
```

Narrow the list to a specific tag first, then fuzzy-pick.

## Shell function shortcut

Add this to your `~/.zshrc` or `~/.bashrc` for a quick `sf` command:

```bash
sf() {
  local title
  title=$(snip --list | fzf --prompt="snip > " --height=40% --reverse) && snip "$title"
}
```

Then just type `sf` to get a fuzzy snippet picker anywhere.
