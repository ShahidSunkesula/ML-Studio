"""
theme.py

Apply ML Studio theme.
"""

import streamlit as st

from src.ui.theme.css import GLOBAL_CSS


def apply_theme() -> None:
    """
    Apply application theme.
    """

    st.markdown(
        GLOBAL_CSS,
        unsafe_allow_html=True,
    )