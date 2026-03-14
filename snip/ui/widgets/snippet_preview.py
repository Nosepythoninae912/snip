from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from snip.models.snippet import Snippet


_LANG_MAP: dict[str, str] = {
    "bash": "bash",
    "c": "c",
    "cpp": "cpp",
    "css": "css",
    "dockerfile": "dockerfile",
    "go": "go",
    "html": "html",
    "java": "java",
    "javascript": "javascript",
    "json": "json",
    "kotlin": "kotlin",
    "markdown": "markdown",
    "php": "php",
    "powershell": "powershell",
    "python": "python",
    "ruby": "ruby",
    "rust": "rust",
    "sql": "sql",
    "swift": "swift",
    "toml": "toml",
    "typescript": "typescript",
    "yaml": "yaml",
    "text": "text",
}


class SnippetPreview(Widget):
    """Right-panel: syntax-highlighted code preview."""

    snippet: reactive[Snippet | None] = reactive(None, layout=True)

    def compose(self) -> ComposeResult:
        yield Static("", id="preview-pin", classes="preview-pin")
        yield Static("", id="preview-title", classes="preview-title")
        yield Static("", id="preview-description", classes="preview-description")
        yield Static("", id="preview-tags", classes="preview-tags")
        with Vertical(classes="preview-code-wrap", id="preview-code-wrap"):
            yield Static("", id="preview-code")
        yield Static("", id="preview-meta", classes="preview-meta")

    def watch_snippet(self, snippet: Snippet | None) -> None:
        if snippet is None:
            self._show_empty()
        else:
            self._render_snippet(snippet)

    def _show_empty(self) -> None:
        self.query_one("#preview-pin", Static).update("")
        self.query_one("#preview-title", Static).update(
            "[#2a2c42]select a snippet to preview[/#2a2c42]"
        )
        self.query_one("#preview-description", Static).update("")
        self.query_one("#preview-tags", Static).update("")
        self.query_one("#preview-code", Static).update("")
        self.query_one("#preview-meta", Static).update("")
        self.query_one("#preview-code-wrap").display = False

    def _render_snippet(self, snippet: Snippet) -> None:
        # pin badge
        self.query_one("#preview-pin", Static).update(
            "[bold #bb9af7]\u2605 pinned[/bold #bb9af7]" if snippet.pinned else ""
        )

        # title
        self.query_one("#preview-title", Static).update(
            f"[bold #e0e7ff]{snippet.title}[/bold #e0e7ff]"
        )

        # description
        desc = snippet.description or ""
        self.query_one("#preview-description", Static).update(
            f"[#565f89]{desc}[/#565f89]" if desc else ""
        )

        # tags
        tags = snippet.tags_display
        self.query_one("#preview-tags", Static).update(
            f"[#73daca]{tags}[/#73daca]" if tags else ""
        )

        # code
        self.query_one("#preview-code-wrap").display = True
        self._render_code(snippet)

        # meta
        created = snippet.created_at.strftime("%Y-%m-%d") if snippet.created_at else ""
        updated = snippet.updated_at.strftime("%Y-%m-%d") if snippet.updated_at else ""
        meta = f"[#3b3f5c]{snippet.language}  \u00b7  {created}"
        if updated and updated != created:
            meta += f"  \u00b7  updated {updated}"
        meta += "[/#3b3f5c]"
        self.query_one("#preview-meta", Static).update(meta)

    def _render_code(self, snippet: Snippet) -> None:
        try:
            from rich.syntax import Syntax

            syntax = Syntax(
                snippet.content,
                _LANG_MAP.get(snippet.language, "text"),
                theme="nord",
                line_numbers=True,
                word_wrap=False,
            )
            self.query_one("#preview-code", Static).update(syntax)
        except Exception:
            self.query_one("#preview-code", Static).update(snippet.content)
