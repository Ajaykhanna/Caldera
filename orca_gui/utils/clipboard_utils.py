"""Clipboard helper markup."""

from __future__ import annotations

import html


def copy_button_html(text: str) -> str:
    """Render a lightweight HTML button that copies supplied text."""
    escaped_text = html.escape(text).replace("\n", "\\n")
    return f"""
    <div class="copy-button-wrap">
      <button class="copy-button" onclick="navigator.clipboard.writeText(`{escaped_text}`)">
        Copy Preview To Clipboard
      </button>
    </div>
    """
