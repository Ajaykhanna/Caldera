#!/usr/bin/env python3
"""Run the ORCA smoke-test input suite in isolated case directories."""

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
