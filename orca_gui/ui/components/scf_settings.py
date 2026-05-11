"""SCF controls."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.orca_keywords import SCF_CONVERGENCE_OPTIONS


def render_scf_settings() -> None:
    """Render curated SCF controls."""
    st.markdown("#### SCF Settings")
    scf_options = [item.keyword for item in SCF_CONVERGENCE_OPTIONS]
    label_lookup = {item.keyword: item.label for item in SCF_CONVERGENCE_OPTIONS}
    if st.session_state.get("scf_convergence") not in scf_options:
        st.session_state["scf_convergence"] = scf_options[1]
    st.selectbox("SCF Convergence", scf_options, format_func=label_lookup.get, key="scf_convergence")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Nprocs", min_value=1, step=1, key="nprocs")
    with col2:
        st.number_input("MaxCore (GB)", min_value=0.25, step=0.25, format="%.2f", key="maxcore")
