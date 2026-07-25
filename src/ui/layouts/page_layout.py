"""
page_layout.py

Purpose:
    Provides a consistent page layout for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_page_layout(
    title: str,
    description: str | None = None,
) -> None:
    """
    Render the standard page layout.
    """

    st.title(title)

    if description:
        st.write(description)

    st.divider()