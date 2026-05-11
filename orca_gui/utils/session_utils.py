"""Session import/export helpers."""

from __future__ import annotations

import json
from typing import Any

from orca_gui.models.session_state import SessionState


def session_json_bytes(state: SessionState) -> bytes:
    """Serialize session state to bytes for download."""
    return json.dumps(state.to_dict(), indent=2).encode("utf-8")


def load_session_json(payload: bytes) -> dict[str, Any]:
    """Load a session mapping from JSON bytes."""
    return json.loads(payload.decode("utf-8"))
