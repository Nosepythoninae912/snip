from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import ListItem, ListView, Static

from snip.models.snippet import Snippet


class SnippetItem(ListItem):
    """A single row in the snippet list."""

    DEFAULT_CSS = """
    SnippetItem {
        height: 4;
        padding: 1 2;
        background: #0d0f18;
        border-bottom: tall #1a1c2e;
    }
    SnippetItem:hover {
        background: #12131e;
    }
    SnippetItem.-highlighted {
        background: #131729;
        border-left: tall #7aa2f7;
        padding-left: 1;
    }
    SnippetItem.-highlighted > .item-title {
        color: #e0e7ff;
    }
    SnippetItem > .item-title {
        color: #a0aabf;
        text-style: bold;
        height: 1;
    }
    SnippetItem > .item-meta {
        color: #3b3f5c;
        height: 1;
    }
    """

    def __init__(self, snippet: Snippet) -> None:
        super().__init__()
        self.snippet = snippet

    def compose(self) -> ComposeResult:
        pin = " [bold #bb9af7]\u2605[/bold #bb9af7]" if self.snippet.pinned else ""
        yield Static(
            f"[bold]{self.snippet.title}[/bold]{pin}",
            markup=True,
            classes="item-title",
        )
        lang = f"[#565f89]{self.snippet.language}[/#565f89]"
        tags = ""
        if self.snippet.tags:
            tags = f"  [#73daca]{self.snippet.tags_display}[/#73daca]"
        yield Static(lang + tags, markup=True, classes="item-meta")


class SnippetList(Widget):
    """Left-panel: navigable list of snippets."""

    DEFAULT_CSS = """
    SnippetList {
        width: 35%;
        min-width: 24;
        border-right: tall #2a2c42;
        background: #0d0f18;
    }
    SnippetList .panel-label {
        height: 1;
        background: #0a0b14;
        color: #2a2c42;
        padding: 0 2;
        border-bottom: tall #1a1c2e;
    }
    SnippetList ListView {
        height: 1fr;
        background: #0d0f18;
        border: none;
        padding: 0;
    }
    SnippetList .empty-label {
        color: #3b3f5c;
        text-align: center;
        padding: 4 2;
    }
    """

    snippets: reactive[list[Snippet]] = reactive([], layout=True)

    def compose(self) -> ComposeResult:
        yield Static("SNIPPETS", classes="panel-label")
        yield ListView(id="list-view")

    def watch_snippets(self, snippets: list[Snippet]) -> None:
        lv: ListView = self.query_one("#list-view", ListView)
        lv.clear()
        if snippets:
            for s in snippets:
                lv.append(SnippetItem(s))
        else:
            lv.append(ListItem(Static("no snippets found", classes="empty-label")))

    def highlighted_snippet(self) -> Snippet | None:
        lv: ListView = self.query_one("#list-view", ListView)
        if lv.highlighted_child is None:
            return None
        item = lv.highlighted_child
        if isinstance(item, SnippetItem):
            return item.snippet
        return None

    def move_down(self) -> None:
        self.query_one("#list-view", ListView).action_cursor_down()

    def move_up(self) -> None:
        self.query_one("#list-view", ListView).action_cursor_up()
