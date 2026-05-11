"""Shared solvation block helpers."""

from __future__ import annotations

from orca_gui.models.session_state import SessionState


def _manual_lines(text: str) -> list[str]:
    """Normalize user-supplied manual block additions."""

    return [line.rstrip() for line in text.splitlines() if line.strip()]


def build_solvation_blocks(state: SessionState) -> list[list[str]]:
    """Render the current solvation block(s) for the selected model."""

    if not state.solvation_enabled:
        return []

    manual_lines = [f"  {line}" for line in _manual_lines(state.custom_cpcm_lines)]

    if state.solvation_model in {"CPCM", "CPCMC"}:
        lines = [f'  solvent "{state.solvent}"']
        if state.cpcm_surface_type != "vdw_gaussian":
            lines.append(f"  surfacetype {state.cpcm_surface_type}")
        lines.extend(manual_lines)
        return [["%cpcm", *lines, "end"]]

    if state.solvation_model == "SMD":
        lines = [
            "  smd true",
            f'  SMDsolvent "{state.solvent}"',
        ]
        lines.extend(manual_lines)
        return [["%cpcm", *lines, "end"]]

    if state.solvation_model == "COSMORS":
        lines = [f'  solvent "{state.solvent}"']
        lines.extend(manual_lines)
        return [["%cosmors", *lines, "end"]]

    return []
