"""Ground-state MD parameter controls."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.orca_keywords import (
    MD_NHC_YOSHIDA_OPTIONS,
    MD_PRINT_LEVEL_OPTIONS,
    MD_SCF_LOG_OPTIONS,
    MD_THERMOSTAT_OPTIONS,
)


def render_md_parameters() -> None:
    """Render manual-backed MD parameters."""
    st.markdown("#### Molecular Dynamics")
    st.caption("Ground-state MD is activated with `MD` on the simple input line and emitted through a `%md` block.")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("MD Timestep (fs)", min_value=0.001, step=0.1, format="%.3f", key="md_timestep_fs")
        st.selectbox(
            "PrintLevel",
            [option.keyword for option in MD_PRINT_LEVEL_OPTIONS],
            key="md_print_level",
        )
        st.checkbox("Initialize Velocities", key="md_initvel_enabled")
        if st.session_state.get("md_initvel_enabled"):
            st.number_input(
                "Initial Velocity Temperature (K)",
                min_value=0.1,
                step=10.0,
                format="%.1f",
                key="md_initvel_temperature_k",
            )
        st.checkbox("Randomize Initial Velocities", key="md_randomize_enabled")
        if st.session_state.get("md_randomize_enabled"):
            st.number_input("Random Seed", min_value=1, step=1, key="md_random_seed")
        st.number_input("MD Run Steps", min_value=1, step=10, key="md_run_steps")

    with col2:
        st.selectbox(
            "Thermostat",
            [option.keyword for option in MD_THERMOSTAT_OPTIONS],
            key="md_thermostat_type",
        )
        if st.session_state.get("md_thermostat_type") != "None":
            st.number_input(
                "Thermostat Temperature (K)",
                min_value=0.1,
                step=10.0,
                format="%.1f",
                key="md_thermostat_temperature_k",
            )
            st.number_input(
                "Time Constant (fs)",
                min_value=0.1,
                step=0.5,
                format="%.1f",
                key="md_timecon_fs",
            )
            if st.session_state.get("md_thermostat_type") == "NHC":
                st.number_input("NHC Chain Length", min_value=1, step=1, key="md_nhc_chain_length")
                st.number_input("NHC MTS", min_value=1, step=1, key="md_nhc_mts")
                st.selectbox(
                    "NHC Yoshida Order",
                    [int(option.keyword) for option in MD_NHC_YOSHIDA_OPTIONS],
                    key="md_nhc_yoshida_order",
                )
        st.selectbox(
            "SCFLog",
            [option.keyword for option in MD_SCF_LOG_OPTIONS],
            key="md_scf_log",
        )
        st.checkbox("Restart IfExists", key="md_restart_if_exists")

    with st.expander("Trajectory Output"):
        st.checkbox("Dump Positions", key="md_dump_position_enabled")
        if st.session_state.get("md_dump_position_enabled"):
            stride_col, file_col = st.columns([1, 2])
            with stride_col:
                st.number_input("Stride", min_value=1, step=1, key="md_dump_position_stride")
            with file_col:
                st.text_input("Trajectory Filename", key="md_dump_position_filename")
