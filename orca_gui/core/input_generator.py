"""Assembly of ORCA input text from validated session state."""

from __future__ import annotations

from dataclasses import dataclass

from orca_gui.config.orca_keywords import STATE_JOB_OPTIONS, solvation_simple_keyword
from orca_gui.core.geometry_parser import geometry_from_state
from orca_gui.core.validator import ORCAValidator, ValidationResult
from orca_gui.generators.dynamics import DynamicsGenerator
from orca_gui.generators.excited_state import build_excited_state_blocks
from orca_gui.generators.ground_state import build_ground_state_blocks
from orca_gui.models.session_state import SessionState


@dataclass(slots=True)
class GeneratedInput:
    """Generated ORCA input plus metadata for the preview panel."""

    text: str
    filename: str
    validation: ValidationResult
    title: str = "Generated Input File"
    mime_type: str = "text/plain"


class ORCAInputGenerator:
    """Generate ORCA input files in the fixed project ordering."""

    def __init__(self, validator: ORCAValidator | None = None) -> None:
        self.validator = validator or ORCAValidator()
        self.dynamics_generator = DynamicsGenerator()

    @staticmethod
    def maxcore_mb(maxcore_gb: float) -> int:
        """Convert UI MaxCore units from GB to ORCA's MB-based input."""
        return max(1, int(round(maxcore_gb * 1024)))

    @staticmethod
    def scf_convergence_block_value(scf_keyword: str) -> str | None:
        """Map simple SCF presets to `%scf Convergence` values."""
        mapping = {
            "TightSCF": "Tight",
            "VeryTightSCF": "VeryTight",
        }
        return mapping.get(scf_keyword)

    @staticmethod
    def method_runtyp_value(job_type: str) -> str:
        """Map the current static job to `%method RunTyp`."""
        mapping = {
            "energy": "Energy",
            "opt": "Opt",
            "freq": "Freq",
        }
        return mapping[job_type]

    @staticmethod
    def _extra_simple_keywords(text: str) -> list[str]:
        """Split custom simple keywords into tokens."""
        return [token for token in text.split() if token]

    @staticmethod
    def _extra_lines(text: str) -> list[str]:
        """Normalize user-supplied extra block lines."""
        return [line.rstrip() for line in text.splitlines() if line.strip()]

    @staticmethod
    def _join_sections(sections: list[list[str]]) -> str:
        """Join top-level ORCA sections with a blank line between blocks."""

        lines: list[str] = []
        for index, section in enumerate(section for section in sections if section):
            if index:
                lines.append("")
            lines.extend(section)
        return "\n".join(lines).strip() + "\n"

    def _build_simple_keywords(self, state: SessionState) -> list[str]:
        """Build the simple input line keywords for the current state."""

        simple_keywords: list[str] = []
        if state.calculation_mode == "dynamics":
            simple_keywords.append("MD")
        simple_keywords.extend([state.method, state.basis_set])
        if state.grid_keyword:
            simple_keywords.append(state.grid_keyword)
        if state.input_design == "simple" and state.scf_convergence:
            simple_keywords.append(state.scf_convergence)
        if (
            state.calculation_mode == "static"
            and state.input_design == "simple"
            and state.static_job_type in STATE_JOB_OPTIONS
            and STATE_JOB_OPTIONS[state.static_job_type]
        ):
            simple_keywords.append(STATE_JOB_OPTIONS[state.static_job_type])
        if state.solvation_enabled:
            simple_keywords.append(solvation_simple_keyword(state.solvation_model, state.solvent))
        simple_keywords.extend(self._extra_simple_keywords(state.custom_simple_keywords))
        return simple_keywords

    def _build_sections_without_geometry(self, state: SessionState) -> list[list[str]]:
        """Build all sections except the final geometry section."""

        sections: list[list[str]] = [
            [f"! {' '.join(self._build_simple_keywords(state))}"],
            [f"%pal nprocs {state.nprocs} end"],
            [f"%maxcore {self.maxcore_mb(state.maxcore)}"],
        ]

        if state.input_design == "block":
            method_lines: list[str] = []
            if state.calculation_mode == "static":
                method_lines.append(f"  RunTyp {self.method_runtyp_value(state.static_job_type)}")
            method_lines.extend(f"  {line}" for line in self._extra_lines(state.custom_method_lines))
            if method_lines:
                sections.append(["%method", *method_lines, "end"])

            scf_lines: list[str] = []
            convergence_value = self.scf_convergence_block_value(state.scf_convergence)
            if convergence_value:
                scf_lines.append(f"  Convergence {convergence_value}")
            scf_lines.extend(f"  {line}" for line in self._extra_lines(state.custom_scf_lines))
            if scf_lines:
                sections.append(["%scf", *scf_lines, "end"])

        if state.calculation_mode == "dynamics":
            sections.extend(self.dynamics_generator.generate_blocks(state))
        elif state.state_type == "excited":
            sections.extend(build_excited_state_blocks(state))
        else:
            sections.extend(build_ground_state_blocks(state))

        extra_raw_blocks = self._extra_lines(state.custom_extra_blocks)
        if extra_raw_blocks:
            sections.append(extra_raw_blocks)
        return sections

    @staticmethod
    def _build_geometry_section(state: SessionState, geometry_source: str, geometry_atoms: list[tuple[str, float, float, float]] | None = None, geometry_filename: str | None = None) -> list[str]:
        """Build the final ORCA geometry section for the selected source."""

        if geometry_source == "uploaded_file":
            return [f"* xyzfile {state.charge} {state.multiplicity} {geometry_filename}"]

        geometry_section = [f"* xyz {state.charge} {state.multiplicity}"]
        for symbol, x_val, y_val, z_val in geometry_atoms or []:
            geometry_section.append(f"{symbol:<2} {x_val: .9f} {y_val: .9f} {z_val: .9f}")
        geometry_section.append("*")
        return geometry_section

    def render_xyzfile_template(self, state: SessionState, xyz_path: str) -> GeneratedInput:
        """Render an ORCA input template that references an external XYZ path."""

        validation = self.validator.validate(state, require_geometry=False)
        if not validation.passed:
            return GeneratedInput(text="", filename=state.output_filename, validation=validation)

        sections = self._build_sections_without_geometry(state)
        sections.append([f"* xyzfile {state.charge} {state.multiplicity} {xyz_path}"])
        text = self._join_sections(sections)
        return GeneratedInput(text=text, filename=state.output_filename, validation=validation)

    def generate(self, state: SessionState) -> GeneratedInput:
        """Validate and render the current ORCA input."""
        validation = self.validator.validate(state)
        if not validation.passed:
            return GeneratedInput(text="", filename=state.output_filename, validation=validation)

        geometry = geometry_from_state(state)
        sections = self._build_sections_without_geometry(state)
        sections.append(
            self._build_geometry_section(
                state,
                geometry_source=geometry.source,
                geometry_atoms=geometry.atoms,
                geometry_filename=geometry.filename,
            )
        )
        text = self._join_sections(sections)
        return GeneratedInput(text=text, filename=state.output_filename, validation=validation)
