# Deployment Preparation

This document captures the practical deployment checklist for the current ORCA GUI milestone after Phases 0-7.

## Local Packaging Checks

- Python target: `>=3.10` from [setup.py](/C:/programs/MyGit/Caldera/setup.py)
- Runtime requirements: `streamlit`, `tqdm`
- Console entry point: `orca-gui=orca_gui.app:main`

Install locally with:

```powershell
C:\Users\401770\AppData\Local\anaconda3\envs\my_env\python.exe -m pip install -r requirements.txt
C:\Users\401770\AppData\Local\anaconda3\envs\my_env\python.exe -m pip install .
```

Run locally with:

```powershell
orca-gui
```

or:

```powershell
C:\Users\401770\AppData\Local\anaconda3\envs\my_env\python.exe -m streamlit run orca_gui\app.py
```

## Validation Checklist

- Regenerate `docs/MANUAL_EXCERPTS.md` if the attached ORCA manual changes.
- Run the full local pytest suite.
- Run `scripts/run_phase8_validation.py` to generate the final readiness report.
- Keep the returned cluster smoke-test `results/` directory with the release bundle for auditability.

## Cluster Caveat

The returned smoke results bundled in `tests/cluster_smoke_bundle/results/` were produced with ORCA `6.0.1`, while the GUI syntax source of truth is the ORCA `6.1` manual. That means:

- the smoke suite is a strong runtime sanity check
- it is not a strict proof of ORCA 6.1 equivalence
- a final release onto a 6.1-capable cluster should rerun the same six smoke inputs with ORCA 6.1 if available

## Recommended Release Bundle

- `orca_gui/`
- `scripts/generate_manual_excerpts.py`
- `scripts/run_phase8_validation.py`
- `docs/MANUAL_EXCERPTS.md`
- `docs/user_guide.md`
- `docs/cluster_smoke_workflow.md`
- `docs/deployment_prep.md`
- `tests/expected_features.md`

## Known Non-Blocking Notes

- Static and MD cluster outputs reported the usual RI auto-assignment warning for `Def2/J`.
- Excited-state NACME cases warned that the run type switches to energy plus gradients; this is expected ORCA behavior.
- The stored MD cluster output still contains the old NHC default warnings because it predates the explicit `Chain`, `MTS`, and `Yoshida` emission now present in the GUI.
