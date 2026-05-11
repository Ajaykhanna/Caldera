"""Static workflow layout."""

from __future__ import annotations

import streamlit as st


def render_static_layout() -> None:
    """Render the static job selector."""
    options = {"Energy": "energy", "Optimization": "opt", "Frequency": "freq"}
    labels = list(options)
    current = st.session_state.get("static_job_type", "energy")
    reverse = {value: key for key, value in options.items()}
    selected = st.radio("Static Job Type", labels, index=labels.index(reverse[current]), horizontal=True)
    st.session_state["static_job_type"] = options[selected]

    if st.session_state.get("state_type") == "excited":
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Nroots", min_value=1, step=1, key="state_average_nroots")
        with col2:
            st.number_input("Iroot", min_value=1, step=1, key="excited_iroot")
        st.caption("ORCA 6.1 enables NACME with `NACME TRUE` under `%TDDFT`; `ETF TRUE` optionally adds built-in electron-translation factors.")
        st.checkbox("NACME True", key="excited_nacme")
        st.checkbox("ETF True", key="excited_etf")
