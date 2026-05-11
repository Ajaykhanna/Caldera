"""Electronic state selector."""

from __future__ import annotations

import streamlit as st


def render_state_selector() -> None:
    """Render ground vs excited state choice."""
    if st.session_state.get("calculation_mode") == "dynamics":
        st.session_state["state_type"] = "ground"
        st.markdown("#### State Selection")
        st.caption("Phase 5 currently supports ground-state molecular dynamics only.")
        return

    options = ["ground", "excited"]
    labels = {"ground": "Ground", "excited": "Excited"}
    if st.session_state.get("state_type") not in options:
        st.session_state["state_type"] = "ground"
    st.radio("State Selection", options, format_func=labels.get, horizontal=True, key="state_type")
