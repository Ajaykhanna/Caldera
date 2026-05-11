"""Level-of-theory selector."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.orca_keywords import METHOD_OPTIONS


def render_level_of_theory() -> None:
    """Render method selection."""
    options = [item.keyword for item in METHOD_OPTIONS]
    if st.session_state.get("method") not in options:
        st.session_state["method"] = options[0]
    st.selectbox("Method", options, key="method")
