"""Ground-state molecular dynamics block generation."""

from __future__ import annotations

from orca_gui.generators.solvation import build_solvation_blocks
from orca_gui.models.session_state import SessionState


def _manual_lines(text: str) -> list[str]:
    """Normalize user-supplied manual MD additions."""

    return [line.rstrip() for line in text.splitlines() if line.strip()]


class DynamicsGenerator:
    """Generate the excerpt-backed ground-state MD block."""

    def generate_blocks(self, state: SessionState) -> list[list[str]]:
        """Return manual-backed `%md` and optional solvation blocks."""

        md_lines = [f"  PrintLevel {state.md_print_level}"]
        if state.md_randomize_enabled:
            md_lines.append(f"  Randomize {state.md_random_seed}")
        md_lines.append(f"  Timestep {state.md_timestep_fs:.3f}_fs")
        if state.md_initvel_enabled:
            md_lines.append(f"  Initvel {state.md_initvel_temperature_k:.1f}_K")
        if state.md_thermostat_type != "None":
            thermostat_line = (
                f"  Thermostat {state.md_thermostat_type} {state.md_thermostat_temperature_k:.1f}_K Timecon {state.md_timecon_fs:.1f}_fs"
            )
            if state.md_thermostat_type == "NHC":
                thermostat_line += (
                    f" Chain {state.md_nhc_chain_length}"
                    f" MTS {state.md_nhc_mts}"
                    f" Yoshida {state.md_nhc_yoshida_order}"
                )
            md_lines.append(thermostat_line)
        md_lines.append(f"  SCFLog {state.md_scf_log}")
        if state.md_dump_position_enabled:
            md_lines.append(
                f'  Dump Position Stride {state.md_dump_position_stride} Filename "{state.md_dump_position_filename}"'
            )
        md_lines.extend(f"  {line}" for line in _manual_lines(state.custom_md_lines))
        if state.md_restart_if_exists:
            md_lines.append("  Restart IfExists")
        md_lines.append(f"  Run {state.md_run_steps}")

        return [["%md", *md_lines, "end"], *build_solvation_blocks(state)]
