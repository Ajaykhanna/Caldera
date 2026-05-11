"""Geometry data model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GeometryData:
    """Normalized geometry information extracted from user input."""

    source: str
    charge: int
    multiplicity: int
    filename: str | None = None
    xyz_text: str | None = None
    atom_count: int | None = None
    atoms: list[tuple[str, float, float, float]] = field(default_factory=list)
