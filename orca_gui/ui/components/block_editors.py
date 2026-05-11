"""Manual block-editing controls."""

from __future__ import annotations

import streamlit as st


def render_block_editors() -> None:
    """Render manual block add-ons for block-style inputs."""
    if st.session_state.get("input_design") != "block":
        return

    with st.expander("Block Design Editors"):
        st.caption(
            "Use these fields to add manual ORCA options inside the generated blocks. Leave them empty to keep the generated defaults only."
        )
        st.text_input("Extra Simple Keywords", key="custom_simple_keywords")
        st.text_area("Extra %method Lines", key="custom_method_lines", height=110)
        st.text_area("Extra %scf Lines", key="custom_scf_lines", height=130)
        if st.session_state.get("calculation_mode") == "dynamics":
            st.text_area("Extra %md Lines", key="custom_md_lines", height=130)
        elif st.session_state.get("state_type") == "excited":
            st.text_area("Extra %tddft Lines", key="custom_tddft_lines", height=130)
        if st.session_state.get("solvation_enabled"):
            solvation_block = "%cosmors" if st.session_state.get("solvation_model") == "COSMORS" else "%cpcm"
            st.text_area(f"Extra {solvation_block} Lines", key="custom_cpcm_lines", height=110)
        st.text_area("Additional Raw Blocks", key="custom_extra_blocks", height=140)
