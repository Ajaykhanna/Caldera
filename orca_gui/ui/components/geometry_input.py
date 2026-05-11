"""Geometry input component."""

from __future__ import annotations

import streamlit as st

from orca_gui.utils.file_utils import decode_xyz_upload


def render_geometry_input() -> None:
    """Render geometry text and file upload inputs."""
    st.markdown("#### Geometry Input")
    st.number_input("Charge", step=1, key="charge")
    st.number_input("Multiplicity", min_value=1, step=1, key="multiplicity")
    st.text_area("Paste XYZ Text", key="geometry_xyz_text", height=220)

    upload = st.file_uploader("Upload XYZ File", type=["xyz"])
    if upload is not None:
        filename, text = decode_xyz_upload(upload.name, upload.getvalue())
        st.session_state["geometry_xyz_filename"] = filename
        st.session_state["geometry_xyz_contents"] = text
    else:
        st.session_state.setdefault("geometry_xyz_contents", "")
