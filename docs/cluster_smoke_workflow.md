# Cluster Smoke Workflow

Phase 7 local development stops at generating and packaging the smoke-test inputs. ORCA execution still happens on the remote cluster.

## Local Bundle Creation

Create the handoff bundle with:

```powershell
C:\Users\401770\AppData\Local\anaconda3\envs\my_env\python.exe scripts\create_cluster_smoke_bundle.py --output-dir tests\cluster_smoke_bundle
```

This writes:

- `tests/cluster_smoke_bundle/inputs/`: the 6 smoke-test `.inp` files
- `tests/cluster_smoke_bundle/manifest.json`: case descriptions
- `tests/cluster_smoke_bundle/run_orca_smoke_suite.py`: cluster-side runner
- `tests/cluster_smoke_bundle/README.md`: quick cluster instructions

## Cluster Execution

On the cluster, copy the bundle and run:

```bash
python run_orca_smoke_suite.py --orca /path/to/orca --overwrite
```

The runner executes each smoke test in an isolated results directory and writes `results/summary.json`.

## What To Return

Return the full `results/` directory after the cluster run, especially:

- `results/summary.json`
- each case directory's `.out` file
- any ORCA auxiliary files that indicate runtime or syntax issues
