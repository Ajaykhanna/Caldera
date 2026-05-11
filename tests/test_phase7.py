"""Phase 7 workflow tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_cluster_smoke_bundle_script_creates_required_handoff_files(repo_root: Path, tmp_path: Path) -> None:
    script_path = repo_root / "scripts" / "create_cluster_smoke_bundle.py"
    output_dir = tmp_path / "cluster_bundle"

    subprocess.run(
        [sys.executable, str(script_path), "--output-dir", str(output_dir)],
        check=True,
        cwd=repo_root,
    )

    manifest_path = output_dir / "manifest.json"
    inputs_dir = output_dir / "inputs"
    runner_path = output_dir / "run_orca_smoke_suite.py"
    readme_path = output_dir / "README.md"

    assert manifest_path.exists()
    assert runner_path.exists()
    assert readme_path.exists()
    assert inputs_dir.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest) == 6
    assert [entry["bundle_name"] for entry in manifest] == [
        "01_static_energy",
        "02_optimization",
        "03_frequency",
        "04_excited_nacme",
        "05_excited_frequency_nacme",
        "06_ground_md",
    ]

    bundled_inputs = sorted(path.name for path in inputs_dir.glob("*.inp"))
    assert bundled_inputs == [
        "01_static_energy.inp",
        "02_optimization.inp",
        "03_frequency.inp",
        "04_excited_nacme.inp",
        "05_excited_frequency_nacme.inp",
        "06_ground_md.inp",
    ]
