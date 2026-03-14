from __future__ import annotations

import datetime

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class AppHeader(Widget):
    """Branded header: ◆ snip logo on the left, live clock on the right."""

    def compose(self) -> ComposeResult:
        yield Static(
            "[bold #7aa2f7]\u25c6[/bold #7aa2f7]"
            " [bold #c0caf5]snip[/bold #c0caf5]"
            "  [#2a2c42]\u00b7  terminal snippet vault[/#2a2c42]",
            markup=True,
            id="app-logo",
        )
        yield Static("", id="app-clock")

    def on_mount(self) -> None:
        self.set_interval(1.0, self._tick)
        self._tick()

    def _tick(self) -> None:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        try:
            self.query_one("#app-clock", Static).update(f"[#3b3f5c]{now}[/#3b3f5c]")
        except Exception:
            pass
