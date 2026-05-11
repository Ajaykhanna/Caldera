"""Advanced options component."""

from __future__ import annotations

import streamlit as st

from orca_gui.config.orca_keywords import (
    CPCM_SURFACE_TYPES,
    SOLVATION_METHOD_OPTIONS,
    get_solvent_option,
    get_supported_solvents,
)


def render_advanced_options() -> None:
    """Render advanced, excerpt-backed options."""
    with st.expander("Advanced Options"):
        st.checkbox("Enable Solvation", key="solvation_enabled")
        if st.session_state.get("solvation_enabled"):
            methods = [item.keyword for item in SOLVATION_METHOD_OPTIONS]
            method_labels = {item.keyword: item.label for item in SOLVATION_METHOD_OPTIONS}
            surfaces = [item.keyword for item in CPCM_SURFACE_TYPES]
            if st.session_state.get("solvation_model") not in methods:
                st.session_state["solvation_model"] = methods[0]
            st.selectbox(
                "Solvation Model",
                methods,
                format_func=method_labels.get,
                key="solvation_model",
            )

            supported_solvents = get_supported_solvents(st.session_state["solvation_model"])
            solvents = [item.keyword for item in supported_solvents]
            solvent_labels = {item.keyword: item.label for item in supported_solvents}
            if st.session_state.get("solvent") not in solvents:
                st.session_state["solvent"] = solvents[0]
            if st.session_state.get("cpcm_surface_type") not in surfaces:
                st.session_state["cpcm_surface_type"] = surfaces[0]
            st.selectbox(
                "Solvent",
                solvents,
                format_func=solvent_labels.get,
                key="solvent",
            )

            solvent = get_solvent_option(st.session_state["solvent"])
            if solvent.dielectric is not None:
                st.caption(
                    f'ORCA internal solvent table entry: `{solvent.keyword}` with dielectric constant {solvent.dielectric:.4f}.'
                )
            else:
                st.caption(
                    f'ORCA internal solvent table entry: `{solvent.keyword}`. The dielectric constant is resolved from the built-in solvent database.'
                )

            if st.session_state["solvation_model"] in {"CPCM", "CPCMC"}:
                st.selectbox(
                    "CPCM Surface Type",
                    surfaces,
                    key="cpcm_surface_type",
                )
            elif st.session_state["solvation_model"] == "SMD":
                st.caption('SMD is emitted through `%cpcm` using `smd true` and `SMDsolvent "..."`.')
            else:
                st.caption('openCOSMO-RS is emitted through a minimal `%cosmors` block for this milestone.')

        st.text_area("Notes", key="notes", height=100)
