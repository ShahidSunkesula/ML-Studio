"""
progress_card.py

Purpose:
    Reusable progress card.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_progress_card(
    title: str,
    value: int | float,
    maximum: int = 100,
):
    """
    Render progress card.
    """

    percentage = value / maximum

    st.markdown(f"#### {title}")

    st.progress(percentage)

    st.caption(
        f"{value:.0f} / {maximum}"
    )