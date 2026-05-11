"""Streamlit entry point."""

from __future__ import annotations

import streamlit as st

from orca_gui.ui.layouts.main_layout import render_main_layout


def main() -> None:
    """Launch the Streamlit application."""
    st.set_page_config(
        page_title="OrcaFlow: Input file Generator",
        page_icon="O",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    render_main_layout()


if __name__ == "__main__":
    main()
