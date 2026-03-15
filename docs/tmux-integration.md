# tmux integration

## Send a snippet to another pane

```bash
tmux send-keys -t {pane} "$(snip -q ports)" Enter
```

Replace `{pane}` with a target like `1` or `top-right`.

## Shell function — pick and send

Add to `~/.zshrc` or `~/.bashrc`:

```bash
snip-tmux() {
  local title content target
  title=$(snip --list | fzf --prompt="send to tmux > " --height=40% --reverse)
  [[ -z "$title" ]] && return
  content=$(snip -q "$title")
  target=$(tmux list-panes -F "#{pane_index}: #{pane_title}" | fzf --prompt="target pane > " --height=20% --reverse | cut -d: -f1)
  [[ -z "$target" ]] && return
  tmux send-keys -t "$target" "$content" Enter
}
```

Call `snip-tmux` to fuzzy-pick a snippet and a target pane, then send it.

## Run a snippet in a new window

```bash
tmux new-window "snip run deploy"
```

## Run a snippet in a split pane

```bash
tmux split-window -h "snip run logs"
```

## tmux keybinding

Add to `~/.tmux.conf` to trigger the fuzzy picker with a prefix key:

```
bind-key S run-shell 'tmux send-keys "$(snip --list | fzf | xargs snip -q)" Enter'
```

Press `prefix + S` to pick a snippet and paste it into the current pane.
