"""Validator tests."""

from __future__ import annotations

from pathlib import Path

from orca_gui.core.validator import ORCAValidator
from orca_gui.core.geometry_parser import parse_xyz_text
from orca_gui.models.session_state import SessionState


def test_geometry_conflict_prefers_uploaded_file(base_state: SessionState, water_xyz: str) -> None:
    state = base_state
    state.geometry_xyz_contents = water_xyz
    state.geometry_xyz_filename = "uploaded.xyz"
    result = ORCAValidator().validate(state)
    assert result.passed
    assert any("uploaded XYZ file" in warning for warning in result.warnings)


def test_missing_geometry_fails(base_state: SessionState) -> None:
    state = base_state
    state.geometry_xyz_text = ""
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("No geometry was provided" in error for error in result.errors)


def test_excited_state_requires_valid_root_range(base_state: SessionState) -> None:
    state = base_state
    state.state_type = "excited"
    state.state_average_nroots = 2
    state.excited_iroot = 3
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("iroot cannot be larger than nroots" in error for error in result.errors)


def test_excited_frequency_nacme_is_allowed_with_warning(base_state: SessionState) -> None:
    state = base_state
    state.state_type = "excited"
    state.static_job_type = "freq"
    state.excited_nacme = True
    result = ORCAValidator().validate(state)
    assert result.passed
    assert any("NACME is intentionally allowed" in warning for warning in result.warnings)


def test_xyz_with_blank_comment_line_is_accepted(repo_root: Path) -> None:
    acetylacetone = (repo_root / "examples" / "acetylacetone.xyz").read_text(encoding="utf-8")
    geometry = parse_xyz_text(acetylacetone, charge=0, multiplicity=1, source="pasted_text")
    assert geometry.atom_count == 15
    assert len(geometry.atoms) == 15


def test_unsupported_solvent_model_pair_fails(base_state: SessionState) -> None:
    state = base_state
    state.solvation_enabled = True
    state.solvation_model = "COSMORS"
    state.solvent = "water"
    state.static_job_type = "opt"
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("openCOSMO-RS limited to energy-style workflows" in error for error in result.errors)


def test_cosmors_is_rejected_for_excited_state(base_state: SessionState) -> None:
    state = base_state
    state.solvation_enabled = True
    state.solvation_model = "COSMORS"
    state.solvent = "Acetonitrile"
    state.state_type = "excited"
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("limited to ground-state static workflows" in error for error in result.errors)


def test_excited_state_md_is_rejected(base_state: SessionState) -> None:
    state = base_state
    state.calculation_mode = "dynamics"
    state.state_type = "excited"
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("ground-state MD only" in error for error in result.errors)


def test_md_random_seed_must_be_positive(base_state: SessionState) -> None:
    state = base_state
    state.calculation_mode = "dynamics"
    state.md_randomize_enabled = True
    state.md_random_seed = 0
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("Random seed must be a positive integer." in error for error in result.errors)


def test_nhc_yoshida_order_must_be_supported(base_state: SessionState) -> None:
    state = base_state
    state.calculation_mode = "dynamics"
    state.md_nhc_yoshida_order = 2
    result = ORCAValidator().validate(state)
    assert not result.passed
    assert any("Unsupported NHC Yoshida order" in error for error in result.errors)
