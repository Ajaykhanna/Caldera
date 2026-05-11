"""Footer component."""

from __future__ import annotations

import streamlit as st


def render_footer() -> None:
    """Render the page footer."""
    st.markdown(
        '<div class="orca-footer">Developer: Ajay Khanna | LANL | May 2026</div>',
        unsafe_allow_html=True,
    )
