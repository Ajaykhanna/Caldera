# User Guide

## What This App Does

The ORCA GUI helps assemble ORCA 6.1 input files for a curated set of ORCA 6.1 workflows:

- ground-state energy
- ground-state optimization
- ground-state frequency
- excited-state TDDFT/CIS-style jobs with optional NACME
- ground-state molecular dynamics
- standalone Python batch-script generation for frame-by-frame XYZ workflows

## Correctness Rule

This milestone only emits syntax that is represented in `docs/MANUAL_EXCERPTS.md`.

## Current Workflow Coverage

The current build supports:

- ground-state static energy, optimization, and frequency jobs
- excited-state TDDFT/CIS-style jobs with optional `NACME TRUE`
- ground-state molecular dynamics with a curated `%md` block using `PrintLevel`, optional `Randomize`, `Timestep`, optional `Initvel`, optional `Thermostat`, `SCFLog`, optional `Dump Position`, optional `Restart IfExists`, and `Run`
- batch-script preview/download mode that emits a standalone Python generator using `argparse`, `tqdm`, absolute XYZ pathing, and no-overwrite safeguards for existing `.inp` files

## Geometry Input Priority

If both pasted XYZ text and an uploaded XYZ file are provided, the uploaded file takes priority and the UI emits a warning.

## Phase 7 Cluster Workflow

Use [docs/cluster_smoke_workflow.md](/C:/programs/MyGit/Caldera/docs/cluster_smoke_workflow.md) to create the smoke-test bundle and run the 6 required ORCA cases on the cluster.

## Phase 8 Readiness

Use `scripts/run_phase8_validation.py` to generate the final readiness report and review [docs/deployment_prep.md](/C:/programs/MyGit/Caldera/docs/deployment_prep.md) before packaging or handoff.
