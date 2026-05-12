# ORCA GUI v6.1 First Milestone Plan (Phases 0-4)

## Summary

Build the first validated milestone as a multi-file Python package in `my_env`, covering Phases 0-4 only: manual-backed correctness infrastructure, package skeleton, core validation/generation, Streamlit UI shell, presets, and advanced static excited-state features.

This milestone will treat `docs/MANUAL_EXCERPTS.md` as the only allowed source of ORCA 6.1 syntax truth. The option catalog will be a curated, manually verified set that covers the required presets, the static smoke tests, and the initial UI controls, rather than a broad freeform catalog.

## Key Changes

### Phase 0: Manual-backed correctness pipeline

- Add `scripts/generate_manual_excerpts.py` as a deterministic extractor with CLI inputs for PDF path and output path.
- Upgrade `my_env` to `streamlit==1.56.0` and add missing parsing dependency support needed for extraction; use the local PDF as input and write `docs/MANUAL_EXCERPTS.md`.
- Scope the excerpt document to GUI-touched sections only:
  - input-file structure and `* xyzfile`
  - geometry optimization
  - vibrational frequency keywords
  - numerical grid guidance including `DEFGRID2`
  - implicit solvation via `CPCM` and `%cpcm`
  - excited-state `%TDDFT` options including `NACME TRUE`
  - molecular dynamics activation and `%md` block, for later phases
- Format excerpts as short sectioned manual snippets with page references and verbatim input examples, so later code can cite exact spellings and placement without guessing.
- Treat any ORCA keyword not represented in the excerpt corpus as out of scope for the first GUI build.

### Phase 1-2: Package foundation and core generation

- Create the package/layout from the blueprint and wire the entrypoint through `orca_gui.app:main`.
- Implement a typed session model centered on `SessionState`, plus a small session-state manager for syncing dataclass values with Streamlit.
- Implement configuration modules for:
  - Sea Side theme constants
  - default UI values
  - curated ORCA keyword catalog backed by the extracted manual sections
- Define stable core interfaces:
  - `ORCAValidator.validate(state) -> ValidationResult`
  - `ORCAInputGenerator.generate(state) -> GeneratedInput`
  - generator helpers for ground-state and excited-state static jobs
- Validation rules in scope for this milestone:
  - uploaded XYZ file overrides pasted XYZ text and emits a warning
  - static job subtype validation for energy, opt, and freq
  - excited-state root/TDDFT validation
  - `NACME` visibility and state handling whenever state is excited
  - curated grid/solvation input validation tied to excerpt-backed options
- Generated output should assemble ORCA input in a fixed order: simple input line, supported blocks, then geometry line/block, with formatting driven by the manual excerpts.

### Phase 3-4: Streamlit UI and advanced static features

- Build the 60/40 two-column Streamlit layout with a sticky right-hand preview/validation panel and Sea Side theme styling.
- Implement the first-pass reusable UI components needed for the milestone:
  - header/footer
  - preset selector
  - calculation type and state selector
  - level of theory and basis selection from the curated catalog
  - geometry input with file-vs-text conflict handling
  - SCF/grid controls
  - implicit solvation controls
  - advanced options panel
  - preview/validation panel
- Ship the 5 preset JSON files and loader, but only fully validate the static presets in this milestone; the ground-state MD preset can exist structurally and be marked phase-gated until Phase 5.
- Advanced static generation in scope:
  - ground-state energy, optimization, and frequency inputs
  - excited-state CIS/TDDFT-style inputs using `%TDDFT`
  - `NACME TRUE` support independent of static subtype selection
  - `CPCM` and `%cpcm` assembly from curated solvent/settings controls
  - grid overrides including `DEFGRID2`-related options only where excerpt-backed
- Use the Browser plugin after the app is runnable to verify desktop/mobile rendering, sticky preview behavior, and the key state transitions in the actual local Streamlit UI.

## Public Interfaces and Types

- `SessionState` remains the central typed state object shared by UI, validator, and generators.
- `ValidationResult` should expose errors, warnings, and pass/fail state in a UI-friendly structure.
- `GeneratedInput` should carry at minimum:
  - rendered `.inp` text
  - suggested filename
  - validation snapshot used for the preview panel
- `scripts/generate_manual_excerpts.py` should support explicit CLI arguments rather than hardcoded paths so the manual pipeline is reproducible.

## Test Plan

- Manual extractor checks:
  - confirm the output includes excerpt-backed sections for `* xyzfile`, `NACME TRUE`, `CPCM`, `DEFGRID2`, and `%md`
  - confirm page references and verbatim example blocks are present
- Core validator tests:
  - geometry text + uploaded file conflict prefers uploaded file and warns
  - invalid/missing geometry is rejected
  - excited-state validation requires the needed TDDFT/root inputs
  - `NACME` is allowed and surfaced whenever excited state is selected
- Generator golden tests for first milestone:
  - static energy, ground state
  - static optimization, ground state
  - static frequency, ground state
  - excited-state CIS energy with `NACME TRUE`
  - excited-state frequency subtype with `NACME` option shown and generated
- UI verification:
  - preset selection populates state correctly
  - preview panel updates from state changes
  - validation panel reflects warnings/errors
  - Browser-based smoke pass confirms layout fidelity and sticky right column behavior
- Defer MD execution/generation smoke tests and batch-script tests to later phases.

## Assumptions and Defaults

- Target runtime is `C:\Users\401770\AppData\Local\anaconda3\envs\my_env` with Python 3.12.3.
- The plan will upgrade that environment to `streamlit==1.56.0` to match the blueprint and add any missing required packages, including PDF parsing support.
- First milestone stops after Phase 4; Phase 5-8 work is intentionally deferred.
- The curated option catalog will prioritize correctness and coverage of presets/smoke tests over breadth.
- ORCA is not available locally, so local acceptance is based on excerpt-backed generation, unit tests, golden outputs, and Browser UI verification; real ORCA execution remains part of the later cluster workflow.
