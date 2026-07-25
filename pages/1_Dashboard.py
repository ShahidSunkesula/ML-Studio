"""
1_Dashboard.py

Purpose:
    Home page for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.ui.layouts.page_layout import (
    PageConfig,
    render_page_layout,
)


def main() -> None:
    """
    Render the Dashboard page.
    """

    render_page_layout(
        PageConfig(
            title="Dashboard",
            description="Overview of your ML Studio project.",
            icon="🏠",
        )
    )

    st.info("Dashboard is under construction.")


if __name__ == "__main__":
    main()