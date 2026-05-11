"""Level-of-theory model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LevelOfTheory:
    """Selected electronic structure settings."""

    method: str
    basis_set: str
    scf_convergence: str = ""
    grid_keyword: str = "DEFGRID2"
