"""
statistic_card.py

Purpose:
    Statistics table card.

Author:
    Shahid

Project:
    ML Studio
"""

import pandas as pd
import streamlit as st


def render_statistic_card(
    title: str,
    dataframe: pd.DataFrame,
) -> None:
    """
    Render statistics card.
    """

    st.markdown(f"### 📈 {title}")

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )