"""Main application layout orchestration."""

from __future__ import annotations

import streamlit as st

from orca_gui.core.batch_processor import BatchProcessor
from orca_gui.core.input_generator import ORCAInputGenerator
from orca_gui.models.session_state import SessionStateManager
from orca_gui.ui.components.advanced_options import render_advanced_options
from orca_gui.ui.components.batch_settings import render_batch_settings
from orca_gui.ui.components.basis_set import render_basis_set
from orca_gui.ui.components.block_editors import render_block_editors
from orca_gui.ui.components.calculation_type import render_calculation_type
from orca_gui.ui.components.footer import render_footer
from orca_gui.ui.components.geometry_input import render_geometry_input
from orca_gui.ui.components.grid_settings import render_grid_settings
from orca_gui.ui.components.header import render_header
from orca_gui.ui.components.input_design import render_input_design
from orca_gui.ui.components.level_of_theory import render_level_of_theory
from orca_gui.ui.components.output_config import render_output_config
from orca_gui.ui.components.preview_panel import render_preview_panel
from orca_gui.ui.components.preset_templates import render_preset_templates
from orca_gui.ui.components.scf_settings import render_scf_settings
from orca_gui.ui.components.state_selector import render_state_selector
from orca_gui.ui.layouts.dynamics_layout import render_dynamics_layout
from orca_gui.ui.layouts.static_layout import render_static_layout
from orca_gui.ui.styles.custom_css import inject_custom_css


def render_main_layout() -> None:
    """Render the full application."""
    SessionStateManager.ensure_defaults()
    inject_custom_css()
    generator = ORCAInputGenerator()
    batch_processor = BatchProcessor()

    render_header()
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.markdown('<div class="orca-left-marker"></div>', unsafe_allow_html=True)
        render_preset_templates()
        render_batch_settings()
        render_calculation_type()
        render_state_selector()
        render_input_design()
        render_level_of_theory()
        render_basis_set()
        if st.session_state.get("calculation_mode") == "static":
            render_static_layout()
        else:
            render_dynamics_layout()
        render_block_editors()
        render_geometry_input()
        render_scf_settings()
        render_grid_settings()
        render_advanced_options()
        render_output_config(SessionStateManager.load())
        button_label = "Generate Batch Script" if st.session_state.get("batch_enabled") else "Generate Input File"
        if st.button(button_label, use_container_width=True):
            st.toast("Preview refreshed.")

    with right_col:
        st.markdown('<div class="orca-right-marker"></div>', unsafe_allow_html=True)
        active_state = SessionStateManager.load()
        generated = batch_processor.generate(active_state) if active_state.batch_enabled else generator.generate(active_state)
        render_preview_panel(generated)

    render_footer()
