"""Excited-state ORCA block generation."""

from __future__ import annotations

from orca_gui.generators.solvation import build_solvation_blocks
from orca_gui.models.session_state import SessionState


def build_excited_state_blocks(state: SessionState) -> list[list[str]]:
    """Render the `%tddft` block and optional CPCM details."""
    block = ["%tddft", f"  nroots {state.state_average_nroots}", f"  iroot {state.excited_iroot}"]
    if state.excited_nacme:
        block.append("  nacme true")
    if state.excited_etf:
        block.append("  etf true")
    if state.excited_grid_override_enabled:
        block.append(f"  GridXC   {state.excited_gridxc}")
        block.append(f"  IntAccXC {state.excited_intaccxc}")
        block.append(f"  GridX    {state.excited_gridx}")
        block.append(f"  IntAccX  {state.excited_intaccx}")
    block.extend(f"  {line}" for line in state.custom_tddft_lines.splitlines() if line.strip())
    block.append("end")

    return [[*block], *build_solvation_blocks(state)]
