<p align="center">
  <img src="Caldera_Logo.png" alt="Caldera Logo" width="220">
</p>

# Caldera: Orca Input file Generator

OrcaFlow is a Streamlit-based GUI package for building ORCA quantum chemistry input files from a curated, manual-backed set of workflows. It is designed to help users assemble consistent ORCA inputs for common ground-state, excited-state, molecular dynamics, and batch-generation tasks without hand-editing every file from scratch.

The project is built around one core correctness rule: GUI-controlled syntax must come from the ORCA 6.1 manual excerpt corpus in `docs/MANUAL_EXCERPTS.md`. The result is a package that aims to be practical for day-to-day setup work while staying anchored to verified ORCA syntax instead of guesswork.

## Live App

Try the hosted Streamlit app here:

- [https://caldera.streamlit.app/](https://caldera.streamlit.app/)

If you just want to use the GUI, visit the live website above. Local installation is only needed if you want to run or modify the app yourself.

## What It Is

- A Python package with a Streamlit frontend
- A curated ORCA input generator for selected ORCA 6.1 workflows
- A manual-backed validation and preview tool
- A batch script generator for multi-frame XYZ workflows
- A tested milestone implementation covering Phases 0-7, with Phase 8 validation tooling included

## What It Does

The GUI currently supports:

- Ground-state static energy inputs
- Ground-state optimization inputs
- Ground-state frequency inputs
- Excited-state TDDFT/CIS-style inputs with `Nroots`, `Iroot`, `NACME TRUE`, and optional `ETF TRUE`
- Ground-state molecular dynamics inputs with curated `%md` controls
- Simple-input and block-design generation paths
- Solvation setup for curated `CPCM`, `CPCMC`, `SMD`, and limited `COSMORS` workflows
- Grid and SCF controls for curated ORCA settings
- Batch generation of a standalone Python script for frame-by-frame `.xyz` to `.inp` workflows

## Design Approach

This package was designed with a few clear constraints:

- Correctness first: GUI syntax is limited to what is represented in `docs/MANUAL_EXCERPTS.md`
- Maintainability: logic is split across `config`, `models`, `core`, `generators`, `ui`, `templates`, and `utils`
- Reproducibility: tests, golden files, manual excerpts, and cluster smoke bundles are all kept in the repository
- Practical workflow support: the GUI includes live preview, validation feedback, preset templates, and batch tooling

## Package Structure

The main package lives in `orca_gui/` and is organized into:

- `config/`: curated ORCA options, defaults, theme constants
- `models/`: typed session state and shared data models
- `core/`: validation, geometry parsing, input assembly, batch processing
- `generators/`: static, excited-state, dynamics, and script-generation logic
- `ui/`: Streamlit components, layouts, and styling
- `templates/`: preset JSON templates
- `scripts/`: manual excerpt generation, cluster bundle generation, and Phase 8 validation tooling
- `docs/`: user-facing documentation and manual-backed reference artifacts
- `tests/`: unit, workflow, batch, Phase 7, and Phase 8 validation tests

## Dependencies

Runtime dependencies are intentionally small:

- `streamlit==1.56.0`
- `tqdm>=4.67,<5`

Development and test dependency currently included in `requirements.txt`:

- `pytest>=8.4,<9`

Python requirement from `setup.py`:

- `Python >= 3.10`

## Installation

### Option 1: Install dependencies and run in place

```powershell
python -m pip install -r requirements.txt
```

### Option 2: Install the package itself

```powershell
python -m pip install .
```

## How To Run

### Run with Streamlit directly

```powershell
streamlit run streamlit_app.py
```

### Run through the package entry point

After `pip install .`:

```powershell
orca-gui
```

## Manual Excerpt Pipeline

The GUI relies on `docs/MANUAL_EXCERPTS.md` as its syntax source of truth.

To regenerate the excerpt corpus from the attached ORCA manual PDF:

```powershell
python scripts/generate_manual_excerpts.py --pdf orca_6.1_may10_2026.pdf --output docs/MANUAL_EXCERPTS.md
```

## Batch Processing

Batch mode does not directly emit hundreds of `.inp` files from the GUI. Instead, it generates a standalone Python script that can be taken to a directory of XYZ frames and run later.

That generated script currently supports:

- `argparse` command-line control
- `tqdm` progress reporting
- absolute XYZ path insertion into generated inputs
- skip-if-existing behavior for `.inp` files by default
- explicit overwrite support through `--overwrite_inps`

Typical workflow:

1. Enable `Batch Processing` in the GUI.
2. Configure frame range, prefixes, and folder pattern.
3. Download the generated Python batch script.
4. Run the script against a frame directory on the target machine.

## Available Features

### Static and Excited-State Features

- Method selection from a curated top-5 functional list
- Basis-set selection from a curated top-5 basis list
- `TightSCF` and `VeryTightSCF` controls
- `DEFGRID1`, `DEFGRID2`, and `DEFGRID3`
- Excited-state root selection
- `NACME TRUE` and optional `ETF TRUE`
- TDDFT expert grid override controls
- Solvation model and solvent selection from the curated manual-backed catalog

### Molecular Dynamics Features

- `MD` activation on the simple input line
- `%md` block generation
- `PrintLevel`
- `Randomize` and random seed
- `Timestep`
- `Initvel`
- Thermostat selection: `Berendsen`, `CSVR`, `NHC`, `None`
- `NHC` defaults and controls for `Chain`, `MTS`, and `Yoshida`
- `SCFLog`
- `Restart IfExists`
- Trajectory dumping controls

### Input and Geometry Features

- Live input preview
- Validation status panel
- Uploaded XYZ file priority over pasted XYZ text
- External `* xyzfile` path generation
- Inline `* xyz` coordinate block generation
- Preset templates for common workflows
- Optional block-design manual editors

## Tests

The repository includes:

- validator tests
- generator golden-file tests
- workflow tests
- batch-script tests
- Phase 7 cluster bundle tests
- Phase 8 readiness tests

Run the full suite with:

```powershell
python -m pytest
```

As of the current repository state, the local suite passes with the full milestone validation layer enabled.

## Cluster Smoke Tests

Phase 7 includes a cluster smoke-test handoff bundle:

```powershell
python scripts/create_cluster_smoke_bundle.py --output-dir tests/cluster_smoke_bundle
```

The bundle contains 6 smoke-test inputs and a cluster-side runner. Returned cluster outputs are stored under `tests/cluster_smoke_bundle/results/`.

Important caveat:

- The returned smoke results currently in the repository were produced with ORCA `6.0.1`
- The GUI syntax source of truth is the ORCA `6.1` manual

So the cluster run is a strong smoke validation, but not a strict ORCA 6.1 equivalence proof.

## Phase 8 Validation

Generate the current final-validation report with:

```powershell
python scripts/run_phase8_validation.py --repo-root . --output docs/PHASE8_VALIDATION.md
```

See:

- `docs/PHASE8_VALIDATION.md`
- `docs/deployment_prep.md`
- `docs/cluster_smoke_workflow.md`

## Developer

Developed by **Ajay Khanna**  
Los Alamos National Laboratory (LANL)  
May 2026

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE).
