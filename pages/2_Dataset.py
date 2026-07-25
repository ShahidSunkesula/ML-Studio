"""
2_Dataset.py

Purpose:
    Dataset Management page for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.core.app_initializer import initialize_page
from src.core.session_manager import SessionManager
from src.services.dataset_service import DatasetService
from src.ui.components.dataset import (
    render_column_summary,
    render_dataset_preview,
    render_dataset_summary,
    render_upload_section,
)
from src.ui.page_layout import PageConfig, render_page_layout


# ==========================================================
# Initialize Page
# ==========================================================

initialize_page()


# ==========================================================
# Page Header
# ==========================================================

render_page_layout(
    PageConfig(
        title="Dataset Management",
        description="Upload and explore your dataset.",
        icon="📂",
    )
)


# ==========================================================
# Upload Dataset
# ==========================================================

uploaded_file = render_upload_section()

if uploaded_file is not None:

    last_uploaded_file = SessionManager.get("last_uploaded_file")

    # Upload only if this file hasn't already been processed
    if last_uploaded_file != uploaded_file.name:

        success = DatasetService.upload_dataset(uploaded_file)

        if success:

            SessionManager.set(
                "last_uploaded_file",
                uploaded_file.name,
            )

            st.rerun()


# ==========================================================
# Retrieve Dataset Information
# ==========================================================

dataset = DatasetService.get_dataset_data()


# ==========================================================
# Dataset Summary
# ==========================================================

render_dataset_summary(dataset)


# ==========================================================
# Dataset Preview
# ==========================================================

render_dataset_preview(dataset)


# ==========================================================
# Column Summary
# ==========================================================

render_column_summary(dataset)