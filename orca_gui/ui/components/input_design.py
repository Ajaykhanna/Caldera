"""Input design controls."""

from __future__ import annotations

import streamlit as st


def render_input_design() -> None:
    """Render the simple-vs-block design switch."""
    options = ["simple", "block"]
    labels = {"simple": "Simple Input", "block": "Block Design"}
    if st.session_state.get("input_design") not in options:
        st.session_state["input_design"] = "simple"
    st.radio("Input Design", options, format_func=labels.get, horizontal=True, key="input_design")

    if st.session_state["input_design"] == "block":
        st.caption(
            "Block design keeps the generated input minimal but exposes editable `%method`, `%scf`, `%tddft`, and `%cpcm` additions."
        )
