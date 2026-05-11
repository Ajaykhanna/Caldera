"""Small validation helpers."""

from __future__ import annotations


def all_present(values: tuple[object | None, ...]) -> bool:
    """Return True if every value is populated."""
    return all(value is not None for value in values)
