"""Path helpers."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the repository root based on the package location."""
    return Path(__file__).resolve().parents[2]
