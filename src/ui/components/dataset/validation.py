"""
validation.py

Professional Dataset Validation Component.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.schemas.dataset import DatasetData
from src.ui.components.common import (
    render_progress_card,
    render_recommendation_card,
    render_section_header,
    render_status_badge,
    render_warning_card,
)


def render_dataset_validation(dataset: DatasetData) -> None:
    """
    Render dataset validation dashboard.
    """

    render_section_header(
        title="Dataset Validation",
        subtitle="Evaluate dataset quality before preprocessing.",
        icon="🛡️",
    )

    ####################################################################
    # Health Score
    ####################################################################

    render_progress_card(
        "Dataset Health Score",
        dataset.health_score,
        100,
    )

    render_status_badge(dataset.health_status)

    st.divider()

    ####################################################################
    # Summary Metrics
    ####################################################################

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Missing Values",
            dataset.missing_values,
        )

    with col2:
        st.metric(
            "Duplicate Rows",
            dataset.duplicate_rows,
        )

    with col3:
        st.metric(
            "Constant Columns",
            dataset.constant_columns,
        )

    with col4:
        st.metric(
            "High Cardinality",
            dataset.high_cardinality_columns,
        )

    st.divider()

    ####################################################################
    # Validation Checks
    ####################################################################

    st.subheader("Validation Results")

    passed = []
    warnings = []

    if dataset.missing_values == 0:
        passed.append("No missing values detected.")
    else:
        warnings.append(
            f"{dataset.missing_values:,} missing values detected."
        )

    if dataset.duplicate_rows == 0:
        passed.append("No duplicate rows detected.")
    else:
        warnings.append(
            f"{dataset.duplicate_rows:,} duplicate rows detected."
        )

    if dataset.constant_columns == 0:
        passed.append("No constant columns detected.")
    else:
        warnings.append(
            f"{dataset.constant_columns} constant columns detected."
        )

    if dataset.empty_columns == 0:
        passed.append("No empty columns detected.")
    else:
        warnings.append(
            f"{dataset.empty_columns} empty columns detected."
        )

    if dataset.high_cardinality_columns == 0:
        passed.append("No high-cardinality columns detected.")
    else:
        warnings.append(
            f"{dataset.high_cardinality_columns} high-cardinality columns detected."
        )

    ###############################################################
    # Passed Checks
    ###############################################################

    if passed:

        st.success("Passed Checks")

        for item in passed:
            st.markdown(f"✅ {item}")

    ###############################################################
    # Warnings
    ###############################################################

    if warnings:

        st.warning("Issues Found")

        for item in warnings:

            render_warning_card(
                "Attention Required",
                item,
            )

    st.divider()

    ####################################################################
    # Recommendations
    ####################################################################

    st.subheader("Recommendations")

    if dataset.missing_values > 0:

        render_recommendation_card(
            "Handle Missing Values",
            "Apply an appropriate imputation technique before model training.",
            "warning",
        )

    if dataset.duplicate_rows > 0:

        render_recommendation_card(
            "Remove Duplicate Rows",
            "Duplicates can bias statistical analysis and machine learning models.",
            "warning",
        )

    if dataset.constant_columns > 0:

        render_recommendation_card(
            "Drop Constant Columns",
            "Constant columns provide no predictive value.",
            "info",
        )

    if dataset.high_cardinality_columns > 0:

        render_recommendation_card(
            "Review High-Cardinality Features",
            "Consider frequency encoding, target encoding, or hashing for these features.",
            "info",
        )

    if (
        dataset.missing_values == 0
        and dataset.duplicate_rows == 0
        and dataset.constant_columns == 0
        and dataset.high_cardinality_columns == 0
    ):

        render_recommendation_card(
            "Excellent Dataset Quality",
            "No major data quality issues were detected. The dataset is ready for preprocessing.",
            "success",
        )