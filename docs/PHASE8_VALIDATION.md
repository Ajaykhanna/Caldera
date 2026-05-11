# Phase 8 Validation Report

Generated on 2026-05-11 by `scripts/run_phase8_validation.py`.

## Scope

This report captures the Phase 8 readiness checks for the current ORCA GUI milestone:

- full local test suite status
- expected feature inventory from `tests/expected_features.md`
- manual excerpt coverage from `docs/MANUAL_EXCERPTS.md`
- returned Phase 7 cluster smoke-test outcomes
- deployment caveats and handoff notes

## Expected Features

- Ground-state static energy generation
- Ground-state optimization generation
- Ground-state frequency generation
- Excited-state TDDFT/CIS-style generation
- NACME True option visible whenever excited state is selected
- Ground-state molecular dynamics generation with `MD` and `%md`
- Standalone Python batch-script generation with absolute XYZ pathing
- Batch no-overwrite safeguards for existing `.inp` files
- Simple input and block-design generation paths
- Uploaded XYZ file priority over pasted XYZ text
- `%pal nprocs` and `%maxcore` generation
- Curated `CPCM`, `CPCMC`, `SMD`, and limited `COSMORS` support
- Curated `DEFGRID1`, `DEFGRID2`, and `DEFGRID3` support
- Top-5 curated DFT functional and basis-set dropdown catalogs
- Manual excerpt generation from the attached ORCA 6.1 PDF

## Manual Compliance Snapshot

Manual excerpt coverage status: pass.

- `xyzfile`: present
- `nacme`: present
- `cpcm`: present
- `smd`: present
- `defgrid`: present
- `md`: present

## Cluster Smoke Results

All 6 returned smoke tests completed successfully.

Observed ORCA version(s) in returned cluster outputs: `6.0.1`

| Case | Return Code | Duration (s) |
| --- | ---: | ---: |
| 01_static_energy | 0 | 9.731 |
| 02_optimization | 0 | 21.581 |
| 03_frequency | 0 | 9.278 |
| 04_excited_nacme | 0 | 7.918 |
| 05_excited_frequency_nacme | 0 | 39.131 |
| 06_ground_md | 0 | 763.050 |

Representative warnings recorded in returned outputs:

- WARNING: Analytical Frequencies for this method not available!
- WARNING: CIS/ROCIS methods need fully converged wavefunctions
- WARNING: Found SCFConvIgnored == true
- WARNING: Geometry Optimization
- WARNING: NACs were selected, the run type will switch to energy+gradients
- WARNING: The environment variable RSH_COMMAND is not set!
- Warning: No MTS count specified. Using 2 as default.
- Warning: No NHC chain length specified. Using 3 as default.

## Deployment Readiness

- Local pytest suite: pass
- Manual excerpt presence check: pass
- Cluster smoke summary return codes: pass
- Packaging entry point present in `setup.py`: `orca-gui=orca_gui.app:main`
- Primary deployment caveat: returned cluster results were produced with ORCA 6.0.1, while the GUI syntax source of truth is the ORCA 6.1 manual.

## Recommended Final Handoff Notes

- Keep `docs/MANUAL_EXCERPTS.md` as the syntax source of truth for GUI-controlled output.
- Treat the ORCA 6.0.1 cluster run as a successful smoke validation, not a strict ORCA 6.1 equivalence proof.
- Before release on a 6.1-capable target, rerun the same smoke suite against ORCA 6.1 if available.
