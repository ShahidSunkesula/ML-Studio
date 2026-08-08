"""
3_Target_Selection.py

Purpose:
    Target variable selection and analysis page.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.core.app_initializer import initialize_page
from src.core.session_manager import SessionManager
from src.ui.components.target import (
    render_target_recommendation,
    render_target_selector,
    render_target_summary,
)
from src.ui.page_layout import (
    PageConfig,
    render_page_layout,
)


# ==========================================================
# Initialize Page
# ==========================================================

initialize_page()


# ==========================================================
# Page Header
# ==========================================================

render_page_layout(
    PageConfig(
        title="Target Selection",
        description=(
            "Select the variable your machine learning "
            "model will predict."
        ),
        icon="🎯",
    )
)


# ==========================================================
# Dataset Check
# ==========================================================

dataset = SessionManager.get("dataset")

if dataset is None:

    st.warning(
        "⚠️ Please upload a dataset before selecting "
        "a target variable."
    )

    st.stop()


# ==========================================================
# Page Navigation
# ==========================================================

selector_tab, summary_tab, recommendation_tab = st.tabs(
    [
        "🎯 Select Target",
        "📊 Target Summary",
        "💡 Recommendations",
    ]
)


# ==========================================================
# Target Selector
# ==========================================================

with selector_tab:

    render_target_selector()


# ==========================================================
# Target Summary
# ==========================================================

with summary_tab:

    render_target_summary()


# ==========================================================
# Recommendations
# ==========================================================

with recommendation_tab:

    render_target_recommendation()


# ==========================================================
# Current Selection
# ==========================================================

st.divider()

target_column = SessionManager.get(
    "target_column"
)

problem_type = SessionManager.get(
    "problem_type"
)

target_selected = SessionManager.get(
    "target_selected",
    False,
)


# ==========================================================
# Selection Status
# ==========================================================

if target_selected and target_column:

    st.success(
        f"✅ Target selected: **{target_column}**"
    )

    if problem_type:

        st.caption(
            f"Detected problem type: **{problem_type}**"
        )

else:

    st.info(
        "Select and save a target variable to continue."
    )