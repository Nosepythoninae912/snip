from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, TextArea

from snip.models.snippet import Snippet, SUPPORTED_LANGUAGES


class EditScreen(ModalScreen[Snippet | None]):
    """Modal form for creating or editing a snippet."""

    DEFAULT_CSS = """
    EditScreen {
        align: center middle;
        background: #0d0f1880;
    }
    EditScreen > Vertical {
        width: 84;
        height: 90%;
        background: #13141f;
        border: tall #2a2c42;
        padding: 1 3;
        overflow-y: auto;
    }
    EditScreen .modal-title {
        text-style: bold;
        color: #7aa2f7;
        padding: 0 0 1 0;
        height: 2;
    }
    EditScreen .modal-divider {
        height: 1;
        color: #2a2c42;
        padding: 0 0 1 0;
    }
    EditScreen .form-label {
        color: #565f89;
        height: 1;
        padding: 0 0 0 0;
    }
    EditScreen Input {
        background: #0d0f18;
        border: tall #2a2c42;
        color: #c0caf5;
        margin-bottom: 1;
    }
    EditScreen Input:focus {
        border: tall #7aa2f7;
        background: #0a0b14;
    }
    EditScreen Select {
        margin-bottom: 1;
    }
    EditScreen Select:focus {
        border: tall #7aa2f7;
    }
    EditScreen TextArea {
        height: 14;
        background: #0d0f18;
        border: tall #2a2c42;
        margin-bottom: 1;
    }
    EditScreen TextArea:focus {
        border: tall #7aa2f7;
    }
    EditScreen .btn-row {
        height: 3;
        align: right middle;
        padding-top: 1;
    }
    EditScreen Button {
        margin-left: 1;
    }
    EditScreen #btn-save {
        background: #7aa2f7;
        color: #0d0f18;
        border: none;
    }
    EditScreen #btn-save:hover {
        background: #5a82d7;
    }
    EditScreen #btn-cancel {
        background: #252640;
        color: #565f89;
        border: none;
    }
    EditScreen #btn-cancel:hover {
        background: #2a2c50;
        color: #c0caf5;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("down", "next_field", show=False),
        Binding("up", "prev_field", show=False),
    ]

    def __init__(self, snippet: Snippet | None = None) -> None:
        super().__init__()
        self._editing = snippet
        self._is_new = snippet is None

    def compose(self) -> ComposeResult:
        s = self._editing
        verb = "new snippet" if self._is_new else "edit snippet"
        with Vertical():
            yield Label(f"\u25c6  {verb}", classes="modal-title")
            yield Label("\u2500" * 60, classes="modal-divider")

            yield Label("title", classes="form-label")
            yield Input(
                value=s.title if s else "",
                placeholder="e.g. reverse a list in Python",
                id="input-title",
            )

            yield Label("language", classes="form-label")
            options = [(lang, lang) for lang in SUPPORTED_LANGUAGES]
            current_lang = s.language if s else "text"
            yield Select(options, value=current_lang, id="input-language")

            yield Label("description", classes="form-label")
            yield Input(
                value=s.description if s else "",
                placeholder="optional short description",
                id="input-description",
            )

            yield Label("tags  (space-separated)", classes="form-label")
            yield Input(
                value=" ".join(s.tags) if s else "",
                placeholder="e.g. python list utils",
                id="input-tags",
            )

            yield Label("code", classes="form-label")
            yield TextArea(
                text=s.content if s else "",
                language=None,
                id="input-content",
                tab_behavior="indent",
            )

            with Horizontal(classes="btn-row"):
                yield Button("cancel", variant="default", id="btn-cancel")
                yield Button("save", variant="primary", id="btn-save")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-save":
            self._save()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def action_next_field(self) -> None:
        if not isinstance(self.focused, TextArea):
            self.focus_next()

    def action_prev_field(self) -> None:
        if not isinstance(self.focused, TextArea):
            self.focus_previous()

    def _save(self) -> None:
        title = self.query_one("#input-title", Input).value.strip()
        if not title:
            self.query_one("#input-title", Input).focus()
            return

        content = self.query_one("#input-content", TextArea).text
        if not content.strip():
            self.query_one("#input-content", TextArea).focus()
            return

        lang_select: Select = self.query_one("#input-language", Select)
        language = str(lang_select.value) if lang_select.value != Select.BLANK else "text"

        description = self.query_one("#input-description", Input).value.strip()
        tags_raw = self.query_one("#input-tags", Input).value.strip()
        tags = [t for t in tags_raw.split() if t]

        if self._editing is not None:
            self._editing.title = title
            self._editing.content = content
            self._editing.language = language
            self._editing.description = description
            self._editing.tags = tags
            self.dismiss(self._editing)
        else:
            self.dismiss(
                Snippet(
                    title=title,
                    content=content,
                    language=language,
                    description=description,
                    tags=tags,
                )
            )
