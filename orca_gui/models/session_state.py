"""Centralized Streamlit session state management."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any

import streamlit as st

from orca_gui.config.settings import DEFAULT_GEOMETRY_FILENAME, DEFAULT_OUTPUT_FILENAME


@dataclass(slots=True)
class SessionState:
    """Typed representation of the current GUI state."""

    preset_name: str = "Static Energy"
    calculation_mode: str = "static"
    input_design: str = "simple"
    static_job_type: str = "energy"
    state_type: str = "ground"
    method: str = "B3LYP"
    basis_set: str = "def2-SVP"
    scf_convergence: str = "TightSCF"
    grid_keyword: str = "DEFGRID2"
    charge: int = 0
    multiplicity: int = 1
    nprocs: int = 4
    maxcore: float = 1.0
    geometry_xyz_text: str = ""
    geometry_xyz_contents: str = ""
    geometry_xyz_filename: str = DEFAULT_GEOMETRY_FILENAME
    solvation_enabled: bool = False
    solvation_model: str = "CPCM"
    solvent: str = "water"
    cpcm_surface_type: str = "vdw_gaussian"
    state_average_nroots: int = 5
    excited_iroot: int = 1
    excited_nacme: bool = False
    excited_etf: bool = False
    excited_grid_override_enabled: bool = False
    excited_gridxc: int | None = None
    excited_intaccxc: float | None = None
    excited_gridx: int | None = None
    excited_intaccx: float | None = None
    custom_simple_keywords: str = ""
    custom_method_lines: str = ""
    custom_scf_lines: str = ""
    custom_tddft_lines: str = ""
    custom_cpcm_lines: str = ""
    custom_extra_blocks: str = ""
    md_timestep_fs: float = 0.5
    md_print_level: str = "Medium"
    md_initvel_enabled: bool = True
    md_initvel_temperature_k: float = 300.0
    md_thermostat_type: str = "NHC"
    md_thermostat_temperature_k: float = 300.0
    md_timecon_fs: float = 10.0
    md_nhc_chain_length: int = 3
    md_nhc_mts: int = 2
    md_nhc_yoshida_order: int = 3
    md_randomize_enabled: bool = True
    md_random_seed: int = 1127
    md_scf_log: str = "Append"
    md_restart_if_exists: bool = False
    md_dump_position_enabled: bool = True
    md_dump_position_stride: int = 1
    md_dump_position_filename: str = "trajectory.xyz"
    md_run_steps: int = 200
    custom_md_lines: str = ""
    output_filename: str = DEFAULT_OUTPUT_FILENAME
    last_validation_summary: str = ""
    last_generated_input: str = ""
    notes: str = ""
    batch_enabled: bool = False
    batch_start_frame: int = 1
    batch_end_frame: int = 1000
    batch_step_frame: int = 1
    batch_output_type: str = "script"
    batch_base_dir: str = ""
    batch_xyz_prefix: str = "frame_"
    batch_subdir_pattern: str = "frame_{}"
    batch_filename_prefix: str = "frame_"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


class SessionStateManager:
    """Synchronize Streamlit session values with the typed state model."""

    @staticmethod
    def _normalize_loaded_values(values: dict[str, Any]) -> dict[str, Any]:
        """Normalize legacy values from earlier milestone revisions."""
        maxcore_value = values.get("maxcore")
        if isinstance(maxcore_value, (int, float)) and maxcore_value > 128:
            values["maxcore"] = round(float(maxcore_value) / 1024.0, 3)
        legacy_thermostat_enabled = values.pop("md_thermostat_enabled", None)
        if legacy_thermostat_enabled is False:
            values["md_thermostat_type"] = "None"
        return values

    @staticmethod
    def ensure_defaults() -> None:
        """Seed Streamlit state with dataclass defaults."""
        defaults = SessionState()
        for name, value in defaults.to_dict().items():
            st.session_state.setdefault(name, value)

    @staticmethod
    def load() -> SessionState:
        """Hydrate the typed session object from Streamlit state."""
        SessionStateManager.ensure_defaults()
        values = SessionStateManager._normalize_loaded_values({
            field.name: st.session_state.get(field.name, field.default)
            for field in fields(SessionState)
        })
        return SessionState(**values)

    @staticmethod
    def save(state: SessionState) -> None:
        """Persist the typed session object back into Streamlit state."""
        for key, value in state.to_dict().items():
            st.session_state[key] = value

    @staticmethod
    def apply_mapping(mapping: dict[str, Any]) -> None:
        """Apply a loaded mapping onto the current Streamlit session."""
        valid_keys = {field.name for field in fields(SessionState)}
        normalized_mapping = SessionStateManager._normalize_loaded_values(dict(mapping))
        for key, value in normalized_mapping.items():
            if key in valid_keys:
                st.session_state[key] = value
