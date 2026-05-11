"""Curated ORCA 6.1 keyword catalog backed by manual excerpts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ManualBackedOption:
    """A curated option explicitly linked to the extracted manual corpus."""

    label: str
    keyword: str
    manual_anchor: str
    note: str = ""


@dataclass(frozen=True)
class SolventOption:
    """A curated solvent entry with method availability metadata."""

    label: str
    keyword: str
    supported_models: frozenset[str]
    manual_anchor: str
    dielectric: float | None = None


METHOD_OPTIONS = (
    ManualBackedOption("B3LYP", "B3LYP", "DFT functional keywords", "Popular global hybrid"),
    ManualBackedOption("PBE0", "PBE0", "DFT functional keywords", "Global hybrid with 25% HF exchange"),
    ManualBackedOption("BP86", "BP86", "DFT functional keywords", "Common GGA functional"),
    ManualBackedOption("BLYP", "BLYP", "DFT functional keywords", "Common GGA functional"),
    ManualBackedOption("PBE", "PBE", "DFT functional keywords", "Common GGA functional"),
)

BASIS_SET_OPTIONS = (
    ManualBackedOption("def2-SV(P)", "def2-SV(P)", "Basis-set keywords", "Reduced-polarization double-zeta"),
    ManualBackedOption("def2-SVP", "def2-SVP", "Basis-set keywords", "Polarized valence double-zeta"),
    ManualBackedOption("def2-TZVP", "def2-TZVP", "Basis-set keywords", "Polarized valence triple-zeta"),
    ManualBackedOption("def2-TZVPP", "def2-TZVPP", "Basis-set keywords", "Doubly polarized valence triple-zeta"),
    ManualBackedOption("cc-pVDZ", "cc-pVDZ", "Basis-set keywords", "Correlation-consistent double-zeta"),
)

SCF_CONVERGENCE_OPTIONS = (
    ManualBackedOption("Default", "", "SCF convergence controls"),
    ManualBackedOption("TightSCF", "TightSCF", "SCF convergence controls"),
    ManualBackedOption("VeryTightSCF", "VeryTightSCF", "SCF convergence controls"),
)

GRID_OPTIONS = (
    ManualBackedOption("DEFGRID1", "DEFGRID1", "DEFGRID guidance", "Old-default sized but more robust"),
    ManualBackedOption("DEFGRID2", "DEFGRID2", "DEFGRID guidance", "Default ORCA 6.1 grid"),
    ManualBackedOption("DEFGRID3", "DEFGRID3", "DEFGRID guidance", "Higher-quality manual-backed grid"),
)

SOLVATION_METHOD_OPTIONS = (
    ManualBackedOption("CPCM", "CPCM", "Solvation method syntax", "Conductor-like PCM"),
    ManualBackedOption("CPCMC", "CPCMC", "Solvation method syntax", "C-PCM with COSMO epsilon function"),
    ManualBackedOption("SMD", "SMD", "Solvation method syntax", "SMD via simple input or %cpcm"),
    ManualBackedOption("COSMORS", "COSMORS", "Solvation method syntax", "openCOSMO-RS workflow"),
)

SOLVENT_OPTIONS = (
    SolventOption("Water", "water", frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"}), "Solvent availability table", 78.3550),
    SolventOption("Methanol", "methanol", frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"}), "Solvent availability table"),
    SolventOption("Ethanol", "ethanol", frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"}), "Solvent availability table"),
    SolventOption("Acetonitrile", "Acetonitrile", frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"}), "Solvent availability table"),
    SolventOption("Tetrahydrofuran (THF)", "THF", frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"}), "Solvent availability table"),
    SolventOption("Carbon Tetrachloride (CCl4)", "ccl4", frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"}), "Solvent availability table"),
)

CPCM_SURFACE_TYPES = (
    ManualBackedOption("Gaussian vdW", "vdw_gaussian", "CPCM input syntax"),
    ManualBackedOption("Gaussian SES", "gepol_ses_gaussian", "CPCM input syntax"),
    ManualBackedOption("Point-charge SES", "gepol_ses", "CPCM input syntax"),
    ManualBackedOption("Point-charge SAS", "gepol_sas", "CPCM input syntax"),
)

STATE_JOB_OPTIONS = {
    "energy": "",
    "opt": "Opt",
    "freq": "Freq",
}

CALCULATION_TYPES = ("static", "dynamics")
STATE_TYPES = ("ground", "excited")

TDDFT_GRID_DEFAULTS = {
    "GridXC": 1,
    "IntAccXC": 3.467,
    "GridX": 1,
    "IntAccX": 3.076,
}

MD_THERMOSTAT_OPTIONS = (
    ManualBackedOption("Berendsen", "Berendsen", "Molecular dynamics thermostat syntax"),
    ManualBackedOption("CSVR", "CSVR", "Molecular dynamics thermostat syntax"),
    ManualBackedOption("NHC", "NHC", "Molecular dynamics thermostat syntax"),
    ManualBackedOption("None", "None", "Molecular dynamics thermostat syntax"),
)

MD_PRINT_LEVEL_OPTIONS = (
    ManualBackedOption("Low", "Low", "Molecular dynamics print level"),
    ManualBackedOption("Medium", "Medium", "Molecular dynamics print level", "Default ORCA 6.1 MD print level"),
    ManualBackedOption("High", "High", "Molecular dynamics print level"),
    ManualBackedOption("Debug", "Debug", "Molecular dynamics print level"),
)

MD_SCF_LOG_OPTIONS = (
    ManualBackedOption("Discard", "Discard", "Molecular dynamics SCF log control"),
    ManualBackedOption("Last", "Last", "Molecular dynamics SCF log control"),
    ManualBackedOption("Append", "Append", "Molecular dynamics SCF log control", "Default ORCA 6.1 MD SCF log mode"),
    ManualBackedOption("Each", "Each", "Molecular dynamics SCF log control"),
)

MD_NHC_YOSHIDA_OPTIONS = (
    ManualBackedOption("1", "1", "Molecular dynamics NHC defaults"),
    ManualBackedOption("3", "3", "Molecular dynamics NHC defaults", "Default ORCA 6.1 NHC Yoshida order"),
    ManualBackedOption("5", "5", "Molecular dynamics NHC defaults"),
    ManualBackedOption("7", "7", "Molecular dynamics NHC defaults"),
)

SOLVATION_BLOCK_MODELS = frozenset({"CPCM", "CPCMC", "SMD", "COSMORS"})


def option_keywords(options: Iterable[ManualBackedOption]) -> tuple[str, ...]:
    """Return the canonical keywords for a manual-backed option collection."""

    return tuple(option.keyword for option in options)


def get_solvent_option(keyword: str) -> SolventOption:
    """Return the curated solvent definition for the selected keyword."""

    for option in SOLVENT_OPTIONS:
        if option.keyword == keyword:
            return option
    raise KeyError(f"Unknown solvent keyword: {keyword}")


def get_supported_solvents(solvation_model: str) -> tuple[SolventOption, ...]:
    """Return solvents available for the selected solvation model."""

    return tuple(option for option in SOLVENT_OPTIONS if solvation_model in option.supported_models)


def solvation_simple_keyword(solvation_model: str, solvent: str) -> str:
    """Return the simple-input solvent invocation for the selected model."""

    solvent_keyword = get_solvent_option(solvent).keyword
    return f"{solvation_model}({solvent_keyword})"
