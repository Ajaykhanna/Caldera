"""Generator golden tests."""

from __future__ import annotations

from pathlib import Path

from orca_gui.core.input_generator import ORCAInputGenerator
from orca_gui.models.session_state import SessionState


def _golden(repo_root: Path, name: str) -> str:
    return (repo_root / "tests" / "golden" / name).read_text(encoding="utf-8")


def test_static_energy_golden(base_state: SessionState, repo_root: Path) -> None:
    state = base_state
    state.output_filename = "static_energy.inp"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert generated.text == _golden(repo_root, "static_energy.inp")


def test_static_optimization_golden(base_state: SessionState, repo_root: Path) -> None:
    state = base_state
    state.static_job_type = "opt"
    state.basis_set = "def2-TZVP"
    state.output_filename = "optimization.inp"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert generated.text == _golden(repo_root, "optimization.inp")


def test_static_frequency_golden(base_state: SessionState, repo_root: Path) -> None:
    state = base_state
    state.static_job_type = "freq"
    state.basis_set = "def2-TZVP"
    state.output_filename = "frequency.inp"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert generated.text == _golden(repo_root, "frequency.inp")


def test_excited_nacme_golden(base_state: SessionState, repo_root: Path) -> None:
    state = base_state
    state.state_type = "excited"
    state.method = "PBE0"
    state.excited_iroot = 2
    state.excited_nacme = True
    state.excited_etf = True
    state.output_filename = "excited_nacme.inp"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert generated.text == _golden(repo_root, "excited_nacme.inp")


def test_excited_frequency_golden(base_state: SessionState, repo_root: Path) -> None:
    state = base_state
    state.state_type = "excited"
    state.static_job_type = "freq"
    state.method = "PBE0"
    state.excited_iroot = 2
    state.excited_nacme = True
    state.excited_etf = True
    state.output_filename = "excited_freq_nacme.inp"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert generated.text == _golden(repo_root, "excited_freq_nacme.inp")


def test_block_design_adds_method_and_scf_blocks(base_state: SessionState) -> None:
    state = base_state
    state.input_design = "block"
    state.static_job_type = "opt"
    state.custom_method_lines = "SpecialGridIntacc 8, 8, 8"
    state.custom_scf_lines = "AutoTRAH true"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert "%method" in generated.text
    assert "RunTyp Opt" in generated.text
    assert "SpecialGridIntacc 8, 8, 8" in generated.text
    assert "%scf" in generated.text
    assert "Convergence Tight" in generated.text
    assert "AutoTRAH true" in generated.text


def test_smd_solvation_writes_simple_and_block_forms(base_state: SessionState) -> None:
    state = base_state
    state.solvation_enabled = True
    state.solvation_model = "SMD"
    state.solvent = "water"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert "SMD(water)" in generated.text
    assert '%cpcm\n  smd true\n  SMDsolvent "water"\nend' in generated.text


def test_percent_blocks_are_separated_by_blank_lines(base_state: SessionState) -> None:
    generated = ORCAInputGenerator().generate(base_state)
    assert generated.validation.passed
    assert "%pal nprocs 4 end\n\n%maxcore 1024" in generated.text


def test_ground_state_md_golden(base_state: SessionState, repo_root: Path) -> None:
    state = base_state
    state.calculation_mode = "dynamics"
    state.output_filename = "ground_md_template.inp"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert generated.text == _golden(repo_root, "ground_md_template.inp")


def test_md_restart_is_emitted_immediately_before_run(base_state: SessionState) -> None:
    state = base_state
    state.calculation_mode = "dynamics"
    state.md_restart_if_exists = True
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert "  Restart IfExists\n  Run 200\nend" in generated.text


def test_nhc_defaults_are_emitted_explicitly(base_state: SessionState) -> None:
    state = base_state
    state.calculation_mode = "dynamics"
    generated = ORCAInputGenerator().generate(state)
    assert generated.validation.passed
    assert "Thermostat NHC 300.0_K Timecon 10.0_fs Chain 3 MTS 2 Yoshida 3" in generated.text
