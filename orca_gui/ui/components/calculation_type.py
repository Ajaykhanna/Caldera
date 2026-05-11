"""Calculation type selector."""

from __future__ import annotations

import streamlit as st


def render_calculation_type() -> None:
    """Render static vs dynamics choice."""
    options = ["static", "dynamics"]
    labels = {"static": "Static", "dynamics": "Dynamics"}
    if st.session_state.get("calculation_mode") not in options:
        st.session_state["calculation_mode"] = "static"
    st.radio("Calculation Type", options, format_func=labels.get, horizontal=True, key="calculation_mode")
