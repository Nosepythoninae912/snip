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


def _make_syntax(content: str, language: str):
    """Return a Rich Syntax renderable styled with the active theme."""
    from rich.syntax import Syntax

    from snip import themes

    t = themes.current
    try:
        from pygments.style import Style
        from pygments.token import (
            Comment,
            Generic,
            Keyword,
            Name,
            Number,
            Operator,
            String,
            Token,
        )
        from rich.syntax import PygmentsSyntaxTheme

        _DynamicStyle = type("_DynamicStyle", (Style,), {
            "background_color": t.surface,
            "default_style": t.text,
            "styles": {
                Token:              t.text,
                Comment:            f"italic {t.text_muted}",
                Keyword:            t.accent,
                Keyword.Constant:   t.syntax_number,
                Keyword.Type:       t.teal,
                Name.Builtin:       t.teal,
                Name.Function:      t.accent,
                Name.Decorator:     t.purple,
                Name.Exception:     t.syntax_error,
                Name.Variable:      t.text,
                String:             t.syntax_string,
                String.Escape:      t.syntax_number,
                Number:             t.syntax_number,
                Operator:           t.syntax_operator,
                Operator.Word:      t.accent,
                Generic.Heading:    f"bold {t.accent}",
                Generic.Subheading: t.teal,
                Generic.Error:      t.syntax_error,
            },
        })
        theme = PygmentsSyntaxTheme(_DynamicStyle)
    except Exception:
        theme = "monokai"  # type: ignore[assignment]

    return Syntax(
        content,
        language,
        theme=theme,
        line_numbers=True,
        word_wrap=False,
    )


class SnippetPreview(Widget):
    """Right-panel: syntax-highlighted code preview."""

    snippet: reactive[Snippet | None] = reactive(None, layout=True)

    def compose(self) -> ComposeResult:
        yield Static("", id="preview-header")
        with Vertical(classes="preview-code-wrap", id="preview-code-wrap"):
            yield Static("", id="preview-code", markup=False)
        yield Static("", id="preview-footer")

    def watch_snippet(self, snippet: Snippet | None) -> None:
        if snippet is None:
            self._show_empty()
        else:
            self._render_snippet(snippet)

    def _show_empty(self) -> None:
        from rich.text import Text

        from snip import themes

        self.query_one("#preview-header", Static).update(
            Text("select a snippet to preview", style=themes.current.text_ghost)
        )
        self.query_one("#preview-footer", Static).update("")
        self.query_one("#preview-code-wrap").display = False

    def _render_snippet(self, snippet: Snippet) -> None:
        from rich.text import Text

        from snip import themes

        t = themes.current
        header = Text()
        if snippet.pinned:
            header.append("\u2605 pinned\n", style=f"bold {t.purple}")
        header.append(snippet.title, style=f"bold {t.text_hi}")
        if snippet.description:
            header.append("\n" + snippet.description, style=t.text_muted)
        if snippet.tags:
            header.append("\n" + snippet.tags_display, style=t.teal)
        self.query_one("#preview-header", Static).update(header)

        self.query_one("#preview-code-wrap").display = True
        self._render_code(snippet)

        created = snippet.created_at.strftime("%Y-%m-%d") if snippet.created_at else ""
        updated = snippet.updated_at.strftime("%Y-%m-%d") if snippet.updated_at else ""
        meta = f"{snippet.language}  \u00b7  {created}"
        if updated and updated != created:
            meta += f"  \u00b7  updated {updated}"
        self.query_one("#preview-footer", Static).update(Text(meta, style=t.text_muted))

    def _render_code(self, snippet: Snippet) -> None:
        from snip import themes
        language = _LANG_MAP.get(snippet.language, "text")
        try:
            syntax = _make_syntax(snippet.content, language)
            self.query_one("#preview-code", Static).update(syntax)
        except Exception:
            from rich.text import Text
            self.query_one("#preview-code", Static).update(
                Text(snippet.content, style=themes.current.text)
            )
