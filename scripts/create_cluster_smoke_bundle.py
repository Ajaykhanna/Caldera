"""Create a Phase 7 cluster smoke-test bundle from the local golden inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent


SMOKE_CASES = (
    ("01_static_energy", "static_energy.inp", "Ground-state static energy"),
    ("02_optimization", "optimization.inp", "Ground-state optimization"),
    ("03_frequency", "frequency.inp", "Ground-state frequency"),
    ("04_excited_nacme", "excited_nacme.inp", "Excited-state TDDFT/CIS with NACME TRUE"),
    ("05_excited_frequency_nacme", "excited_freq_nacme.inp", "Excited-state frequency with NACME option"),
    ("06_ground_md", "ground_md_template.inp", "Ground-state molecular dynamics template"),
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Create the Phase 7 ORCA cluster smoke-test bundle.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory that will receive the smoke-test bundle.")
    return parser.parse_args()


def repo_root() -> Path:
    """Return the repository root from the scripts directory."""

    return Path(__file__).resolve().parents[1]


def runner_script_text() -> str:
    """Return the cluster runner script text."""

    return dedent(
        """\
        #!/usr/bin/env python3
        \"\"\"Run the ORCA smoke-test input suite in isolated case directories.\"\"\"

        from __future__ import annotations

        import argparse
        import json
        import shutil
        import subprocess
        import sys
        import time
        from pathlib import Path


        def parse_args() -> argparse.Namespace:
            parser = argparse.ArgumentParser(description="Run the ORCA smoke-test suite.")
            parser.add_argument("--orca", required=True, help="Path to the ORCA executable on the cluster.")
            parser.add_argument("--inputs-dir", default="inputs", help="Directory containing the smoke-test .inp files.")
            parser.add_argument("--results-dir", default="results", help="Directory where per-case outputs will be written.")
            parser.add_argument("--overwrite", action="store_true", help="Delete an existing results directory before running.")
            return parser.parse_args()


        def main() -> int:
            args = parse_args()
            inputs_dir = Path(args.inputs_dir).resolve()
            results_dir = Path(args.results_dir).resolve()

            if not inputs_dir.exists():
                raise SystemExit(f"Input directory not found: {inputs_dir}")

            if results_dir.exists():
                if not args.overwrite:
                    raise SystemExit(f"Results directory already exists: {results_dir}. Use --overwrite to replace it.")
                shutil.rmtree(results_dir)
            results_dir.mkdir(parents=True, exist_ok=True)

            summary: list[dict[str, object]] = []
            failures = 0

            for input_path in sorted(inputs_dir.glob("*.inp")):
                case_dir = results_dir / input_path.stem
                case_dir.mkdir(parents=True, exist_ok=True)
                local_inp = case_dir / input_path.name
                shutil.copy2(input_path, local_inp)

                stdout_path = case_dir / f"{input_path.stem}.out"
                stderr_path = case_dir / f"{input_path.stem}.stderr.log"
                started = time.time()

                completed = subprocess.run(
                    [args.orca, local_inp.name],
                    cwd=case_dir,
                    capture_output=True,
                    text=True,
                )

                stdout_path.write_text(completed.stdout, encoding="utf-8", errors="replace")
                stderr_path.write_text(completed.stderr, encoding="utf-8", errors="replace")

                duration_s = round(time.time() - started, 3)
                generated_files = sorted(path.name for path in case_dir.iterdir())
                summary.append(
                    {
                        "case": input_path.stem,
                        "input_file": input_path.name,
                        "returncode": completed.returncode,
                        "duration_s": duration_s,
                        "generated_files": generated_files,
                    }
                )
                if completed.returncode != 0:
                    failures += 1

            summary_path = results_dir / "summary.json"
            summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
            print(f"Wrote smoke-test summary to {summary_path}")
            if failures:
                print(f"{failures} smoke test(s) failed.")
                return 1
            print("All smoke tests completed successfully.")
            return 0


        if __name__ == "__main__":
            raise SystemExit(main())
        """
    )


def bundle_readme_text() -> str:
    """Return the bundle README text."""

    return dedent(
        """\
        # ORCA Phase 7 Smoke-Test Bundle

        This bundle contains the 6 smoke-test ORCA input files required by the Phase 7 blueprint.

        ## Contents

        - `inputs/`: the ORCA `.inp` smoke-test files
        - `manifest.json`: case descriptions
        - `run_orca_smoke_suite.py`: cluster-side runner that executes each case in its own results directory

        ## Cluster Usage

        1. Copy this bundle to the cluster.
        2. Load the ORCA environment on the cluster.
        3. Run:

           ```bash
           python run_orca_smoke_suite.py --orca /path/to/orca --overwrite
           ```

        4. Send back the entire `results/` directory, especially:

           - `results/summary.json`
           - each case directory's `.out` file
           - any ORCA-generated auxiliary files that indicate parser/runtime issues
        """
    )


def create_bundle(output_dir: Path) -> None:
    """Create the smoke-test bundle contents."""

    root = repo_root()
    golden_dir = root / "tests" / "golden"
    inputs_dir = output_dir / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, str]] = []
    for bundle_name, golden_name, description in SMOKE_CASES:
        source = golden_dir / golden_name
        target = inputs_dir / f"{bundle_name}.inp"
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        manifest.append(
            {
                "bundle_name": bundle_name,
                "source_golden": golden_name,
                "description": description,
            }
        )

    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (output_dir / "run_orca_smoke_suite.py").write_text(runner_script_text(), encoding="utf-8")
    (output_dir / "README.md").write_text(bundle_readme_text(), encoding="utf-8")


def main() -> None:
    """CLI entry point."""

    args = parse_args()
    create_bundle(args.output_dir.resolve())


if __name__ == "__main__":
    main()
