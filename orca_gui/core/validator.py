"""Validation for the curated ORCA 6.1 feature set."""

from __future__ import annotations

from dataclasses import dataclass, field

from orca_gui.config.orca_keywords import (
    BASIS_SET_OPTIONS,
    GRID_OPTIONS,
    MD_NHC_YOSHIDA_OPTIONS,
    MD_PRINT_LEVEL_OPTIONS,
    MD_SCF_LOG_OPTIONS,
    MD_THERMOSTAT_OPTIONS,
    METHOD_OPTIONS,
    SCF_CONVERGENCE_OPTIONS,
    SOLVATION_METHOD_OPTIONS,
    get_supported_solvents,
)
from orca_gui.core.geometry_parser import geometry_from_state
from orca_gui.models.session_state import SessionState


@dataclass(slots=True)
class ValidationResult:
    """Validation messages and status for the current state."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Whether validation succeeded."""
        return not self.errors

    def add_error(self, message: str) -> None:
        """Record a blocking validation error."""
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Record a non-blocking validation warning."""
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        """Record an informational message."""
        self.infos.append(message)


class ORCAValidator:
    """Validate session state against curated manual-backed rules."""

    def validate(self, state: SessionState, require_geometry: bool = True) -> ValidationResult:
        """Run the full validation suite."""
        result = ValidationResult()
        self._validate_catalog(state, result)
        self._validate_resources(state, result)
        if require_geometry:
            self._validate_geometry(state, result)
        self._validate_calculation_mode(state, result)
        self._validate_excited_state(state, result)
        self._validate_solvation(state, result)
        self._validate_dynamics(state, result)
        return result

    def _validate_catalog(self, state: SessionState, result: ValidationResult) -> None:
        valid_methods = {item.keyword for item in METHOD_OPTIONS}
        valid_basis = {item.keyword for item in BASIS_SET_OPTIONS}
        valid_scf = {item.keyword for item in SCF_CONVERGENCE_OPTIONS}
        valid_grids = {item.keyword for item in GRID_OPTIONS}
        valid_solvation_models = {item.keyword for item in SOLVATION_METHOD_OPTIONS}
        valid_md_thermostats = {item.keyword for item in MD_THERMOSTAT_OPTIONS}
        valid_md_print_levels = {item.keyword for item in MD_PRINT_LEVEL_OPTIONS}
        valid_md_scf_logs = {item.keyword for item in MD_SCF_LOG_OPTIONS}
        valid_md_yoshida_orders = {int(item.keyword) for item in MD_NHC_YOSHIDA_OPTIONS}
        if state.method not in valid_methods:
            result.add_error(f"Unsupported method selection: {state.method}")
        if state.basis_set not in valid_basis:
            result.add_error(f"Unsupported basis-set selection: {state.basis_set}")
        if state.scf_convergence not in valid_scf:
            result.add_error(f"Unsupported SCF convergence selection: {state.scf_convergence}")
        if state.grid_keyword not in valid_grids:
            result.add_error(f"Unsupported grid selection: {state.grid_keyword}")
        if state.solvation_model not in valid_solvation_models:
            result.add_error(f"Unsupported solvation model selection: {state.solvation_model}")
        if state.md_thermostat_type not in valid_md_thermostats:
            result.add_error(f"Unsupported MD thermostat selection: {state.md_thermostat_type}")
        if state.md_print_level not in valid_md_print_levels:
            result.add_error(f"Unsupported MD PrintLevel selection: {state.md_print_level}")
        if state.md_scf_log not in valid_md_scf_logs:
            result.add_error(f"Unsupported MD SCFLog selection: {state.md_scf_log}")
        if state.md_nhc_yoshida_order not in valid_md_yoshida_orders:
            result.add_error(f"Unsupported NHC Yoshida order: {state.md_nhc_yoshida_order}")

    def _validate_resources(self, state: SessionState, result: ValidationResult) -> None:
        if state.nprocs < 1:
            result.add_error("nprocs must be at least 1.")
        if state.maxcore <= 0:
            result.add_error("MaxCore must be greater than 0 GB.")
        if state.multiplicity < 1:
            result.add_error("Multiplicity must be at least 1.")

    def _validate_geometry(self, state: SessionState, result: ValidationResult) -> None:
        if state.geometry_xyz_contents and state.geometry_xyz_text.strip():
            result.add_warning(
                "Both uploaded file and pasted text provided. Prioritizing the uploaded XYZ file."
            )
        try:
            geometry_from_state(state)
        except ValueError as exc:
            result.add_error(str(exc))

    def _validate_calculation_mode(self, state: SessionState, result: ValidationResult) -> None:
        if state.calculation_mode == "dynamics" and state.state_type != "ground":
            result.add_error("The current dynamics milestone supports ground-state MD only.")

    def _validate_excited_state(self, state: SessionState, result: ValidationResult) -> None:
        if state.state_type != "excited":
            return
        if state.state_average_nroots < 1:
            result.add_error("Excited-state calculations require nroots >= 1.")
        if state.excited_iroot < 1:
            result.add_error("Excited-state calculations require iroot >= 1.")
        if state.excited_iroot > state.state_average_nroots:
            result.add_error("iroot cannot be larger than nroots.")

        override_fields = (
            state.excited_gridxc,
            state.excited_intaccxc,
            state.excited_gridx,
            state.excited_intaccx,
        )
        if state.excited_grid_override_enabled and not all(value is not None for value in override_fields):
            result.add_error("TDDFT grid overrides require GridXC, IntAccXC, GridX, and IntAccX together.")

        if state.static_job_type == "freq" and state.excited_nacme:
            result.add_warning(
                "NACME is intentionally allowed for excited-state frequency jobs per project requirements."
            )

    def _validate_solvation(self, state: SessionState, result: ValidationResult) -> None:
        if not state.solvation_enabled:
            return
        if not state.solvent:
            result.add_error("A solvent must be selected when solvation is enabled.")
            return

        supported_solvents = {option.keyword for option in get_supported_solvents(state.solvation_model)}
        if state.solvent not in supported_solvents:
            result.add_error(
                f'The solvent "{state.solvent}" is not available for {state.solvation_model} in the curated manual-backed catalog.'
            )

        if state.solvation_model == "COSMORS" and state.state_type == "excited":
            result.add_error("The first milestone keeps openCOSMO-RS limited to ground-state static workflows.")
        if state.solvation_model == "COSMORS" and state.static_job_type != "energy":
            result.add_error("The first milestone keeps openCOSMO-RS limited to energy-style workflows.")
        if state.solvation_model == "COSMORS" and state.calculation_mode == "dynamics":
            result.add_error("The current dynamics milestone does not support openCOSMO-RS workflows.")

    def _validate_dynamics(self, state: SessionState, result: ValidationResult) -> None:
        if state.calculation_mode != "dynamics":
            return
        if state.md_timestep_fs <= 0:
            result.add_error("MD Timestep (fs) must be greater than 0.")
        if state.md_initvel_enabled and state.md_initvel_temperature_k <= 0:
            result.add_error("Initial velocity temperature (K) must be greater than 0.")
        if state.md_thermostat_type != "None" and state.md_thermostat_temperature_k <= 0:
            result.add_error("Thermostat temperature (K) must be greater than 0.")
        if state.md_thermostat_type != "None" and state.md_timecon_fs <= 0:
            result.add_error("Thermostat time constant (fs) must be greater than 0.")
        if state.md_thermostat_type == "NHC" and state.md_nhc_chain_length < 1:
            result.add_error("NHC chain length must be at least 1.")
        if state.md_thermostat_type == "NHC" and state.md_nhc_mts < 1:
            result.add_error("NHC MTS must be at least 1.")
        if state.md_randomize_enabled and state.md_random_seed < 1:
            result.add_error("Random seed must be a positive integer.")
        if state.md_dump_position_enabled and state.md_dump_position_stride < 1:
            result.add_error("Trajectory stride must be at least 1.")
        if state.md_run_steps < 1:
            result.add_error("MD Run steps must be at least 1.")
