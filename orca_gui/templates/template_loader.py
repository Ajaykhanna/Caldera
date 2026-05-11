"""Preset template loading."""

from __future__ import annotations

import json
from pathlib import Path

from orca_gui.utils.path_utils import repo_root


def _template_dir() -> Path:
    return repo_root() / "orca_gui" / "templates"


def list_preset_names() -> list[str]:
    """Return friendly preset names in display order."""
    return [
        "Static Energy",
        "Optimization",
        "Frequency",
        "Excited State",
        "Ground-State MD",
    ]


def load_preset(name: str) -> dict[str, object]:
    """Load a named preset file."""
    mapping = {
        "Static Energy": "preset_static_energy.json",
        "Optimization": "preset_opt.json",
        "Frequency": "preset_freq.json",
        "Excited State": "preset_excited_state.json",
        "Ground-State MD": "preset_ground_md.json",
    }
    file_name = mapping[name]
    return json.loads((_template_dir() / file_name).read_text(encoding="utf-8"))
