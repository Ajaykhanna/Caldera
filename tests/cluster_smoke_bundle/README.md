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
