"""Basis set selector."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.orca_keywords import BASIS_SET_OPTIONS


def render_basis_set() -> None:
    """Render basis-set selection."""
    options = [item.keyword for item in BASIS_SET_OPTIONS]
    if st.session_state.get("basis_set") not in options:
        st.session_state["basis_set"] = options[0]
    st.selectbox("Basis-Set", options, key="basis_set")
