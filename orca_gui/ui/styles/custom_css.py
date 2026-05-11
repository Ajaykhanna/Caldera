"""Custom CSS injection."""

from __future__ import annotations

import streamlit as st

from orca_gui.ui.styles.theme import css_variables


def inject_custom_css() -> None:
    """Inject the custom CSS theme and layout behavior."""
    st.markdown(
        f"""
        <style>
        {css_variables()}

        .stApp {{
          background:
            radial-gradient(circle at top left, rgba(83, 210, 220, 0.18), transparent 32%),
            linear-gradient(180deg, rgba(79, 143, 192, 0.08), rgba(248, 250, 251, 0.96));
          color: var(--orca-text-dark);
        }}

        h2, h3, h4 {{
          color: var(--orca-primary-dark);
        }}

        .orca-header-shell,
        .orca-footer {{
          background: rgba(255, 255, 255, 0.92);
          border: 1px solid rgba(79, 143, 192, 0.18);
          border-radius: 18px;
          box-shadow: 0 18px 40px rgba(38, 100, 142, 0.08);
        }}

        .orca-header-shell {{
          padding: 1.15rem 1.3rem 0.85rem 1.3rem;
          margin-bottom: 1rem;
        }}

        .orca-header-shell h1 {{
          margin: 0;
          color: var(--orca-primary-dark);
          font-size: 2.2rem;
          line-height: 1.15;
        }}

        div[data-testid="column"]:has(.orca-right-marker) > div[data-testid="stVerticalBlock"] {{
          position: sticky;
          top: 1rem;
          background: rgba(255, 255, 255, 0.92);
          border: 1px solid rgba(79, 143, 192, 0.18);
          border-radius: 18px;
          box-shadow: 0 18px 40px rgba(38, 100, 142, 0.08);
          padding: 1rem 1.1rem;
        }}

        div[data-testid="column"]:has(.orca-right-marker) h3 {{
          color: var(--orca-primary-dark);
          margin-top: 0.2rem;
        }}

        .orca-preview-code {{
          background: #f5f8fb;
          border: 1px solid rgba(79, 143, 192, 0.18);
          border-radius: 12px;
          font-family: "Cascadia Code", "Consolas", monospace;
          font-size: 0.95rem;
          line-height: 1.5;
          overflow-x: auto;
          padding: 1rem;
        }}

        .orca-preview-empty {{
          color: var(--orca-text-light);
        }}

        .orca-simple-line,
        .orca-directive-line,
        .orca-python-banner-line,
        .orca-python-comment-line,
        .orca-python-docstring-line,
        .orca-python-structure-line,
        .orca-code-line {{
          border-radius: 10px;
          margin-bottom: 0.3rem;
          overflow-wrap: anywhere;
          padding: 0.22rem 0.45rem;
          white-space: pre-wrap;
        }}

        .orca-simple-line {{
          background: linear-gradient(135deg, rgba(83, 210, 220, 0.24), rgba(79, 143, 192, 0.14));
          border-left: 4px solid var(--orca-primary-medium);
          color: #154462;
          font-weight: 700;
        }}

        .orca-directive-line {{
          background: rgba(38, 100, 142, 0.07);
          color: #1d4f73;
        }}

        .orca-code-line {{
          color: #20465f;
        }}

        .orca-python-banner-line {{
          background: linear-gradient(135deg, rgba(38, 100, 142, 0.88), rgba(83, 210, 220, 0.38));
          color: white;
          font-weight: 700;
        }}

        .orca-python-comment-line {{
          background: rgba(255, 227, 179, 0.28);
          color: #7b4e11;
        }}

        .orca-python-docstring-line {{
          background: rgba(83, 210, 220, 0.16);
          color: #17617c;
        }}

        .orca-python-structure-line {{
          background: rgba(38, 100, 142, 0.11);
          color: #154462;
          font-weight: 600;
        }}

        .orca-status {{
          border-radius: 12px;
          margin-top: 0.65rem;
          padding: 0.8rem 0.9rem;
        }}

        .status-success {{
          background: rgba(16, 185, 129, 0.14);
          color: #0f5132;
        }}

        .status-error {{
          background: rgba(239, 68, 68, 0.12);
          color: #9f1239;
        }}

        .status-warning {{
          background: rgba(245, 158, 11, 0.14);
          color: #92400e;
        }}

        .status-info {{
          background: rgba(79, 143, 192, 0.12);
          color: #1d4f73;
        }}

        .orca-footer {{
          margin-top: 1.5rem;
          padding: 0.8rem 1rem;
          text-align: center;
          color: var(--orca-text-light);
        }}

        .stButton > button,
        .stDownloadButton > button {{
          background: linear-gradient(135deg, var(--orca-primary-dark), var(--orca-primary-medium));
          border: none;
          border-radius: 12px;
          color: white;
          font-weight: 600;
        }}

        [data-testid="stExpander"] {{
          border-radius: 16px;
          border: 1px solid rgba(79, 143, 192, 0.16);
          background: rgba(255, 255, 255, 0.8);
        }}

        @media (max-width: 960px) {{
          div[data-testid="column"]:has(.orca-right-marker) > div[data-testid="stVerticalBlock"] {{
            position: static;
            padding: 0;
            background: transparent;
            border: none;
            box-shadow: none;
          }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
