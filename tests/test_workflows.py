"""Workflow and integration checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from orca_gui.templates.template_loader import list_preset_names, load_preset


def test_manual_extractor_generates_required_sections(repo_root: Path, tmp_path: Path) -> None:
    pdf_path = repo_root / "orca_6.1_may10_2026.pdf"
    output_path = tmp_path / "MANUAL_EXCERPTS.md"
    script_path = repo_root / "scripts" / "generate_manual_excerpts.py"
    subprocess.run(
        [sys.executable, str(script_path), "--pdf", str(pdf_path), "--output", str(output_path)],
        check=True,
        cwd=repo_root,
    )
    content = output_path.read_text(encoding="utf-8")
    assert "Input Structure and XYZ File Syntax" in content
    assert "NACME   TRUE" in content
    assert "! CPCM(solvent)" in content
    assert "! SMD(solvent)" in content
    assert "DEFGRID2" in content
    assert "DFT Functional Keywords" in content
    assert "Basis-set Keywords" in content
    assert "%md" in content


def test_preset_loader_exposes_required_templates() -> None:
    names = list_preset_names()
    assert names == [
        "Static Energy",
        "Optimization",
        "Frequency",
        "Excited State",
        "Ground-State MD",
    ]
    excited = load_preset("Excited State")
    assert excited["state_type"] == "excited"
    assert excited["preset_name"] == "Excited State"
