"""Preset selector component."""

from __future__ import annotations

import streamlit as st

from orca_gui.models.session_state import SessionStateManager
from orca_gui.templates.template_loader import list_preset_names, load_preset


def render_preset_templates() -> None:
    """Render and apply curated preset templates."""
    preset_names = list_preset_names()
    current_name = st.session_state.get("preset_name", preset_names[0])
    if current_name not in preset_names:
        current_name = preset_names[0]

    selection = st.selectbox("Preset Templates", preset_names, index=preset_names.index(current_name))
    if selection != st.session_state.get("preset_name"):
        SessionStateManager.apply_mapping(load_preset(selection))
        st.session_state["preset_name"] = selection
        st.toast(f"Applied preset: {selection}")
        st.rerun()
