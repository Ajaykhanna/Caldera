"""Ground-state ORCA block generation."""

from __future__ import annotations

from orca_gui.generators.solvation import build_solvation_blocks
from orca_gui.models.session_state import SessionState


def build_ground_state_blocks(state: SessionState) -> list[list[str]]:
    """Render supported ground-state blocks."""
    return build_solvation_blocks(state)
