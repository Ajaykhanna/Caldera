"""Output and session import/export controls."""

from __future__ import annotations

import streamlit as st

from orca_gui.models.session_state import SessionState, SessionStateManager
from orca_gui.utils.session_utils import load_session_json, session_json_bytes


def render_output_config(state: SessionState) -> None:
    """Render filename plus save/load session configuration tools."""
    st.text_input("Output Filename", key="output_filename")
    with st.expander("Save / Load Session"):
        st.download_button(
            "Download Session JSON",
            data=session_json_bytes(state),
            file_name="orca_gui_session.json",
            mime="application/json",
        )
        uploaded = st.file_uploader("Load Session JSON", type=["json"], key="session_json_upload")
        if uploaded is not None and st.button("Apply Loaded Session"):
            SessionStateManager.apply_mapping(load_session_json(uploaded.getvalue()))
            st.toast("Loaded session configuration.")
            st.rerun()
