from __future__ import annotations

from textual.app import ComposeResult
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

    DEFAULT_CSS = """
    SnippetPreview {
        width: 1fr;
        background: #0d0f18;
        padding: 1 2;
        overflow-y: auto;
    }
    SnippetPreview .preview-pin {
        color: #bb9af7;
        height: 1;
    }
    SnippetPreview .preview-title {
        color: #e0e7ff;
        text-style: bold;
        height: 1;
        padding: 0 0 1 0;
    }
    SnippetPreview .preview-description {
        color: #565f89;
        height: 1;
        padding: 0 0 1 0;
    }
    SnippetPreview .preview-tags {
        color: #73daca;
        height: 1;
        padding: 0 0 1 0;
    }
    SnippetPreview .preview-code-wrap {
        border: tall #2a2c42;
        background: #0a0b14;
        padding: 0 1;
        margin: 0 0 1 0;
    }
    SnippetPreview .preview-meta {
        color: #3b3f5c;
        height: 1;
        padding: 1 0 0 0;
    }
    SnippetPreview .preview-empty {
        color: #2a2c42;
        text-align: center;
        padding: 6 2;
    }
    """

    snippet: reactive[Snippet | None] = reactive(None, layout=True)

    def compose(self) -> ComposeResult:
        yield Static("", id="preview-pin", classes="preview-pin")
        yield Static("", id="preview-title", classes="preview-title")
        yield Static("", id="preview-description", classes="preview-description")
        yield Static("", id="preview-tags", classes="preview-tags")
        with __import__("textual.containers", fromlist=["Vertical"]).Vertical(
            classes="preview-code-wrap", id="preview-code-wrap"
        ):
            yield Static("", id="preview-code")
        yield Static("", id="preview-meta", classes="preview-meta")

    def watch_snippet(self, snippet: Snippet | None) -> None:
        if snippet is None:
            self._show_empty()
            return
        self._render_snippet(snippet)

    def _show_empty(self) -> None:
        self.query_one("#preview-pin", Static).update("")
        self.query_one("#preview-title", Static).update(
            "[dim]select a snippet to preview[/dim]"
        )
        self.query_one("#preview-description", Static).update("")
        self.query_one("#preview-tags", Static).update("")
        self.query_one("#preview-code", Static).update("")
        self.query_one("#preview-meta", Static).update("")
        self.query_one("#preview-code-wrap").display = False

    def _render_snippet(self, snippet: Snippet) -> None:
        if snippet.pinned:
            self.query_one("#preview-pin", Static).update(
                "[bold #bb9af7]\u2605 pinned[/bold #bb9af7]"
            )
        else:
            self.query_one("#preview-pin", Static).update("")

        self.query_one("#preview-title", Static).update(
            f"[bold #e0e7ff]{snippet.title}[/bold #e0e7ff]"
        )

        desc = snippet.description or ""
        self.query_one("#preview-description", Static).update(
            f"[#565f89]{desc}[/#565f89]" if desc else ""
        )

        tags_text = snippet.tags_display
        self.query_one("#preview-tags", Static).update(
            f"[#73daca]{tags_text}[/#73daca]" if tags_text else ""
        )

        self.query_one("#preview-code-wrap").display = True
        self._render_code(snippet)

        created = snippet.created_at.strftime("%Y-%m-%d") if snippet.created_at else ""
        updated = snippet.updated_at.strftime("%Y-%m-%d") if snippet.updated_at else ""
        self.query_one("#preview-meta", Static).update(
            f"[#3b3f5c]{snippet.language}  \u00b7  {created}"
            + (f"  \u00b7  updated {updated}" if updated != created else "")
            + "[/#3b3f5c]"
        )

    def _render_code(self, snippet: Snippet) -> None:
        try:
            from rich.syntax import Syntax

            lexer = _LANG_MAP.get(snippet.language, "text")
            syntax = Syntax(
                snippet.content,
                lexer,
                theme="nord",
                line_numbers=True,
                word_wrap=False,
            )
            self.query_one("#preview-code", Static).update(syntax)
        except Exception:
            self.query_one("#preview-code", Static).update(snippet.content)
