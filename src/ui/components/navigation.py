"""
navigation.py

Purpose:
    Renders workflow-aware navigation for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.core.workflow_manager import WorkflowManager


PAGES = [
    ("Dashboard", None),
    ("Dataset", "dataset_uploaded"),
    ("Preprocessing", "dataset_profiled"),
    ("Feature Engineering", "preprocessing_completed"),
    ("Model Training", "feature_engineering_completed"),
    ("Prediction", "model_trained"),
    ("Reports", "prediction_completed"),
]


def render_navigation() -> str:
    """
    Render navigation and return the selected page.
    """

    available_pages = []

    for page_name, required_stage in PAGES:

        if required_stage is None:
            available_pages.append(page_name)

        elif WorkflowManager.is_completed(required_stage):
            available_pages.append(page_name)

    selected_page = st.sidebar.radio(
        "Navigation",
        available_pages,
    )

    return selected_page