"""Batch settings controls for standalone script generation."""

from __future__ import annotations

import streamlit as st


def render_batch_settings() -> None:
    """Render Phase 6 batch-processing controls."""
    with st.expander("Batch Processing"):
        st.checkbox("Enable Batch Processing", key="batch_enabled")
        if not st.session_state.get("batch_enabled"):
            st.caption("Enable this section to preview and download a standalone Python batch generator.")
            return

        st.info("Phase 6 currently generates a standalone Python script that walks frame directories, skips existing .inp files by default, and supports `--overwrite_inps` when replacement is desired.")
        st.selectbox("Batch Output", ["script"], key="batch_output_type")

        frame_col1, frame_col2, frame_col3 = st.columns(3)
        with frame_col1:
            st.number_input("Start Frame", min_value=1, step=1, key="batch_start_frame")
        with frame_col2:
            st.number_input("End Frame", min_value=1, step=1, key="batch_end_frame")
        with frame_col3:
            st.number_input("Step Frame", min_value=1, step=1, key="batch_step_frame")

        st.text_input("Example Base Directory", key="batch_base_dir", help="Used in the preview comment only. The generated script still accepts --base_dir explicitly at runtime.")

        naming_col1, naming_col2 = st.columns(2)
        with naming_col1:
            st.text_input("XYZ Prefix", key="batch_xyz_prefix")
            st.text_input("Output Prefix", key="batch_filename_prefix")
        with naming_col2:
            st.text_input("Subdirectory Pattern", key="batch_subdir_pattern", help='Examples: `frame_{}` or leave blank to look directly in `base_dir`.')
