"""Geometry parsing helpers for XYZ content."""

from __future__ import annotations

from pathlib import Path

from orca_gui.models.geometry import GeometryData
from orca_gui.models.session_state import SessionState


def parse_xyz_text(xyz_text: str, charge: int, multiplicity: int, source: str, filename: str | None = None) -> GeometryData:
    """Parse plain XYZ text into a normalized geometry structure."""
    lines = [line.rstrip() for line in xyz_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) < 2:
        raise ValueError("XYZ content must contain at least an atom count and one atom line.")

    try:
        atom_count = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError("The first XYZ line must be an integer atom count.") from exc

    after_count = lines[1:]
    atom_lines = [line for line in after_count[1:] if line.strip()]
    if len(atom_lines) != atom_count:
        fallback_atom_lines = [line for line in after_count if line.strip()]
        if len(fallback_atom_lines) == atom_count:
            atom_lines = fallback_atom_lines
    if len(atom_lines) != atom_count:
        raise ValueError(f"XYZ atom count mismatch: expected {atom_count}, found {len(atom_lines)} atom lines.")

    atoms: list[tuple[str, float, float, float]] = []
    for index, line in enumerate(atom_lines, start=1):
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Atom line {index} must contain an element and three coordinates.")
        symbol = parts[0]
        try:
            x_val, y_val, z_val = (float(parts[1]), float(parts[2]), float(parts[3]))
        except ValueError as exc:
            raise ValueError(f"Atom line {index} contains a non-numeric coordinate.") from exc
        atoms.append((symbol, x_val, y_val, z_val))

    return GeometryData(
        source=source,
        charge=charge,
        multiplicity=multiplicity,
        filename=filename,
        xyz_text="\n".join(lines),
        atom_count=atom_count,
        atoms=atoms,
    )


def geometry_from_state(state: SessionState) -> GeometryData:
    """Resolve geometry priority from the current session state."""
    if state.geometry_xyz_contents:
        filename = Path(state.geometry_xyz_filename or "geometry.xyz").name
        return parse_xyz_text(
            xyz_text=state.geometry_xyz_contents,
            charge=state.charge,
            multiplicity=state.multiplicity,
            source="uploaded_file",
            filename=filename,
        )
    if state.geometry_xyz_text.strip():
        return parse_xyz_text(
            xyz_text=state.geometry_xyz_text,
            charge=state.charge,
            multiplicity=state.multiplicity,
            source="pasted_text",
        )
    raise ValueError("No geometry was provided.")
