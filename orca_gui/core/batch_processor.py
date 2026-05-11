"""Batch-processing helpers for Phase 6 script generation."""

from __future__ import annotations

from orca_gui.core.input_generator import GeneratedInput
from orca_gui.core.validator import ORCAValidator, ValidationResult
from orca_gui.generators.script_generator import BatchScriptGenerator
from orca_gui.models.session_state import SessionState


class BatchProcessor:
    """Validate batch settings and build the standalone batch-script preview."""

    def __init__(self, validator: ORCAValidator | None = None) -> None:
        self.validator = validator or ORCAValidator()

    def is_available(self) -> bool:
        """Return whether batch processing is implemented."""

        return True

    def validate(self, state: SessionState) -> ValidationResult:
        """Validate the selected batch settings plus non-geometry ORCA settings."""

        result = self.validator.validate(state, require_geometry=False)

        if state.batch_output_type != "script":
            result.add_error("Phase 6 currently supports script-based batch generation only.")
        if state.batch_start_frame < 1:
            result.add_error("Batch start frame must be at least 1.")
        if state.batch_end_frame < state.batch_start_frame:
            result.add_error("Batch end frame must be greater than or equal to the start frame.")
        if state.batch_step_frame < 1:
            result.add_error("Batch step frame must be at least 1.")
        try:
            if state.batch_subdir_pattern:
                state.batch_subdir_pattern.format(state.batch_start_frame)
        except Exception as exc:
            result.add_error(f"Batch subdirectory pattern must be formattable with a frame number: {exc}")

        return result

    def generate(self, state: SessionState) -> GeneratedInput:
        """Generate the Phase 6 batch-script preview artifact."""

        validation = self.validate(state)
        filename = BatchScriptGenerator.output_filename(state)
        if not validation.passed:
            return GeneratedInput(
                text="",
                filename=filename,
                validation=validation,
                title="Generated Batch Script",
                mime_type="text/x-python",
            )

        script_text = BatchScriptGenerator(state, input_generator=None).generate()
        return GeneratedInput(
            text=script_text,
            filename=filename,
            validation=validation,
            title="Generated Batch Script",
            mime_type="text/x-python",
        )
