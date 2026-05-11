"""Header component."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.settings import APP_TITLE


def render_header() -> None:
    """Render the page header."""
    st.markdown(
        f"""
        <section class="orca-header-shell">
          <h1>{APP_TITLE}</h1>
        </section>
        """,
        unsafe_allow_html=True,
    )
