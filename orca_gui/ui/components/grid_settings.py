"""Grid settings component."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.orca_keywords import GRID_OPTIONS, TDDFT_GRID_DEFAULTS


def render_grid_settings() -> None:
    """Render curated grid controls."""
    st.markdown("#### Grid Settings")
    options = [item.keyword for item in GRID_OPTIONS]
    if st.session_state.get("grid_keyword") not in options:
        st.session_state["grid_keyword"] = options[0]
    st.selectbox("Grid Keyword", options, key="grid_keyword")

    if st.session_state.get("state_type") == "excited":
        with st.expander("TDDFT Expert Grid Overrides"):
            st.caption("These map to GridXC, IntAccXC, GridX, and IntAccX in the %TDDFT block.")
            enable_override = st.checkbox("Enable explicit TDDFT grid override values", key="excited_grid_override_enabled")
            if enable_override:
                if st.session_state.get("excited_gridxc") is None:
                    st.session_state["excited_gridxc"] = TDDFT_GRID_DEFAULTS["GridXC"]
                if st.session_state.get("excited_intaccxc") is None:
                    st.session_state["excited_intaccxc"] = TDDFT_GRID_DEFAULTS["IntAccXC"]
                if st.session_state.get("excited_gridx") is None:
                    st.session_state["excited_gridx"] = TDDFT_GRID_DEFAULTS["GridX"]
                if st.session_state.get("excited_intaccx") is None:
                    st.session_state["excited_intaccx"] = TDDFT_GRID_DEFAULTS["IntAccX"]
                col1, col2 = st.columns(2)
                with col1:
                    st.number_input("GridXC", min_value=1, step=1, key="excited_gridxc")
                    st.number_input("GridX", min_value=1, step=1, key="excited_gridx")
                with col2:
                    st.number_input("IntAccXC", min_value=0.1, step=0.1, key="excited_intaccxc")
                    st.number_input("IntAccX", min_value=0.1, step=0.1, key="excited_intaccx")
            else:
                st.session_state["excited_gridxc"] = None
                st.session_state["excited_intaccxc"] = None
                st.session_state["excited_gridx"] = None
                st.session_state["excited_intaccx"] = None
