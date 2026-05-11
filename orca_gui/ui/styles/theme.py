"""Theme helpers."""

from __future__ import annotations

from orca_gui.config.constants import (
    ACCENT_CYAN,
    ACCENT_WARM,
    BACKGROUND,
    PRIMARY_DARK,
    PRIMARY_MEDIUM,
    TEXT_DARK,
    TEXT_LIGHT,
)


def css_variables() -> str:
    """Return the CSS variable block for the app theme."""
    return f"""
    :root {{
      --orca-primary-dark: {PRIMARY_DARK};
      --orca-primary-medium: {PRIMARY_MEDIUM};
      --orca-accent-cyan: {ACCENT_CYAN};
      --orca-accent-warm: {ACCENT_WARM};
      --orca-background: {BACKGROUND};
      --orca-text-dark: {TEXT_DARK};
      --orca-text-light: {TEXT_LIGHT};
    }}
    """
