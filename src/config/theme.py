"""
theme.py

Purpose:
    Defines the visual theme and shared CSS for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.config.constants import PRIMARY_COLOR


CSS = f"""
<style>

.main {{
    padding-top: 1rem;
}}

h1 {{
    color: {PRIMARY_COLOR};
}}

h2 {{
    color: {PRIMARY_COLOR};
}}

.stButton > button {{
    width: 100%;
    border-radius: 10px;
    font-weight: 600;
}}

.stMetric {{
    border: 1px solid #dddddd;
    border-radius: 10px;
    padding: 12px;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

</style>
"""


def apply_theme() -> None:
    """
    Apply the ML Studio theme.
    """
    st.markdown(CSS, unsafe_allow_html=True)