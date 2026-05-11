"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from orca_gui.models.session_state import SessionState


@pytest.fixture()
def water_xyz() -> str:
    return "\n".join(
        [
            "3",
            "water",
            "O 0.000000 0.000000 0.000000",
            "H 0.000000 0.757160 0.586260",
            "H 0.000000 -0.757160 0.586260",
        ]
    )


@pytest.fixture()
def base_state(water_xyz: str) -> SessionState:
    return SessionState(
        geometry_xyz_text=water_xyz,
        output_filename="test.inp",
        maxcore=1.0,
    )


@pytest.fixture()
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]
