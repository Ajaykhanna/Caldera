"""File handling helpers."""

from __future__ import annotations

import json
from pathlib import Path


def decode_xyz_upload(file_name: str, payload: bytes) -> tuple[str, str]:
    """Decode uploaded XYZ file bytes into UTF-8 text."""
    text = payload.decode("utf-8")
    return Path(file_name).name, text


def decode_json_upload(payload: bytes) -> dict[str, object]:
    """Decode a JSON configuration upload."""
    return json.loads(payload.decode("utf-8"))
