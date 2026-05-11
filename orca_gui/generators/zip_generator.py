"""ZIP helpers for later batch workflows."""

from __future__ import annotations

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile


def zip_named_text(filename: str, text: str) -> bytes:
    """Return a zip archive containing a single text file."""
    buffer = BytesIO()
    with ZipFile(buffer, mode="w", compression=ZIP_DEFLATED) as archive:
        archive.writestr(filename, text)
    return buffer.getvalue()
