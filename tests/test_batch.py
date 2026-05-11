"""Batch-processing tests for Phase 6."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from orca_gui.core.batch_processor import BatchProcessor


def test_batch_script_preview_does_not_require_sample_geometry(base_state) -> None:
    state = base_state
    state.batch_enabled = True
    state.geometry_xyz_text = ""
    artifact = BatchProcessor().generate(state)
    assert artifact.validation.passed
    assert artifact.title == "Generated Batch Script"
    assert artifact.mime_type == "text/x-python"
    assert "* xyzfile 0 1 {XYZ_PATH}" in artifact.text


def test_batch_script_contains_phase6_guards(base_state) -> None:
    state = base_state
    state.batch_enabled = True
    state.batch_end_frame = 3
    artifact = BatchProcessor().generate(state)
    assert artifact.validation.passed
    assert "argparse.ArgumentParser" in artifact.text
    assert "from tqdm import tqdm" in artifact.text
    assert "--overwrite_inps" in artifact.text
    assert "if inp_file.exists() and not args.overwrite_inps:" in artifact.text
    assert "os.path.abspath" in artifact.text


def test_generated_batch_script_creates_absolute_xyz_inputs_and_skips_existing(base_state, water_xyz: str, tmp_path: Path) -> None:
    state = base_state
    state.batch_enabled = True
    state.batch_end_frame = 2
    artifact = BatchProcessor().generate(state)
    assert artifact.validation.passed

    script_path = tmp_path / artifact.filename
    script_path.write_text(artifact.text, encoding="utf-8")

    base_dir = tmp_path / "frames"
    frame_one_dir = base_dir / "frame_1"
    frame_two_dir = base_dir / "frame_2"
    frame_one_dir.mkdir(parents=True)
    frame_two_dir.mkdir(parents=True)
    xyz_one = frame_one_dir / "frame_1.xyz"
    xyz_two = frame_two_dir / "frame_2.xyz"
    xyz_one.write_text(water_xyz, encoding="utf-8")
    xyz_two.write_text(water_xyz, encoding="utf-8")

    existing_inp = frame_two_dir / "frame_2.inp"
    existing_inp.write_text("already-here", encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(script_path), "--base_dir", str(base_dir)],
        capture_output=True,
        text=True,
        check=True,
    )

    generated_inp = frame_one_dir / "frame_1.inp"
    assert generated_inp.exists()
    generated_text = generated_inp.read_text(encoding="utf-8")
    assert f"* xyzfile 0 1 {xyz_one.resolve()}" in generated_text
    assert existing_inp.read_text(encoding="utf-8") == "already-here"
    assert "Summary: 1 Generated, 1 Skipped, 0 Failures." in completed.stdout


def test_generated_batch_script_overwrites_when_flag_is_passed(base_state, water_xyz: str, tmp_path: Path) -> None:
    state = base_state
    state.batch_enabled = True
    state.batch_end_frame = 1
    artifact = BatchProcessor().generate(state)
    assert artifact.validation.passed

    script_path = tmp_path / artifact.filename
    script_path.write_text(artifact.text, encoding="utf-8")

    base_dir = tmp_path / "frames"
    frame_one_dir = base_dir / "frame_1"
    frame_one_dir.mkdir(parents=True)
    xyz_one = frame_one_dir / "frame_1.xyz"
    xyz_one.write_text(water_xyz, encoding="utf-8")

    existing_inp = frame_one_dir / "frame_1.inp"
    existing_inp.write_text("already-here", encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(script_path), "--base_dir", str(base_dir), "--overwrite_inps"],
        capture_output=True,
        text=True,
        check=True,
    )

    generated_text = existing_inp.read_text(encoding="utf-8")
    assert "already-here" not in generated_text
    assert f"* xyzfile 0 1 {xyz_one.resolve()}" in generated_text
    assert "Summary: 1 Generated, 0 Skipped, 0 Failures." in completed.stdout
