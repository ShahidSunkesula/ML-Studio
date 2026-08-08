"""
preview.py

Purpose:
    Professional dataset preview component.

Author:
    Shahid

Project:
    ML Studio
"""

from io import BytesIO

import pandas as pd
import streamlit as st

from src.schemas.dataset import DatasetData
from src.ui.components.common import (
    render_empty_state,
    render_section_header,
)


# ==========================================================
# Download Helper
# ==========================================================


def _download_preview(df: pd.DataFrame) -> None:
    """
    Provide a CSV download for the currently displayed preview.
    """

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Preview",
        data=BytesIO(csv_data),
        file_name="dataset_preview.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ==========================================================
# Dataset Preview
# ==========================================================


def render_dataset_preview(dataset: DatasetData) -> None:
    """
    Render an interactive preview of the uploaded dataset.
    """

    # ======================================================
    # Section Header
    # ======================================================

    render_section_header(
        title="Dataset Preview",
        subtitle="Explore your uploaded dataset interactively.",
        icon="📋",
    )

    # ======================================================
    # Empty State
    # ======================================================

    if dataset.preview is None or dataset.preview.empty:

        render_empty_state(
            title="No Dataset Available",
            message="Upload a dataset to preview its contents.",
            icon="📂",
        )

        return

    preview = dataset.preview.copy()

    # ======================================================
    # Controls
    # ======================================================

    col1, col2, col3 = st.columns([1, 1.2, 1])

    # ------------------------------------------------------
    # Number of Rows
    # ------------------------------------------------------

    with col1:

        rows = st.selectbox(
            "Rows",
            options=[5, 10, 20, 50, 100],
            index=1,
            key="dataset_preview_rows",
        )

    # ------------------------------------------------------
    # Column Search
    # ------------------------------------------------------

    with col2:

        search = st.text_input(
            "🔍 Search Columns",
            placeholder="Search by column name...",
            key="dataset_preview_search",
        )

    # ------------------------------------------------------
    # Column Selection
    # ------------------------------------------------------

    with col3:

        column_options = [
            "All Columns",
            *list(preview.columns),
        ]

        selected_columns = st.multiselect(
            "🧩 Columns",
            options=column_options,
            default=["All Columns"],
            key="dataset_preview_columns",
        )

    # ======================================================
    # Apply Column Search
    # ======================================================

    if search:

        matching_columns = [
            column
            for column in preview.columns
            if search.lower() in str(column).lower()
        ]

        if not matching_columns:

            st.warning(
                f"No columns found matching **{search}**."
            )

            return

        preview = preview[matching_columns]

    # ======================================================
    # Apply Column Selection
    # ======================================================

    if (
        "All Columns" not in selected_columns
        and selected_columns
    ):

        available_columns = [
            column
            for column in selected_columns
            if column in preview.columns
        ]

        if available_columns:

            preview = preview[available_columns]

    # ======================================================
    # Preview Tabs
    # ======================================================

    head_tab, tail_tab, sample_tab, statistics_tab = st.tabs(
        [
            "⬆ Head",
            "⬇ Tail",
            "🎲 Random Sample",
            "📊 Statistics",
        ]
    )

    # ======================================================
    # Head
    # ======================================================

    with head_tab:

        st.caption(
            f"First {min(rows, len(preview))} rows"
        )

        st.dataframe(
            preview.head(rows),
            use_container_width=True,
            hide_index=True,
        )

    # ======================================================
    # Tail
    # ======================================================

    with tail_tab:

        st.caption(
            f"Last {min(rows, len(preview))} rows"
        )

        st.dataframe(
            preview.tail(rows),
            use_container_width=True,
            hide_index=True,
        )

    # ======================================================
    # Random Sample
    # ======================================================

    with sample_tab:

        sample_size = min(rows, len(preview))

        st.caption(
            f"Random sample of {sample_size} rows"
        )

        if sample_size > 0:

            st.dataframe(
                preview.sample(
                    n=sample_size,
                    random_state=42,
                ),
                use_container_width=True,
                hide_index=True,
            )

    # ======================================================
    # Statistics
    # ======================================================

    with statistics_tab:

        numeric = preview.select_dtypes(
            include="number"
        )

        if numeric.empty:

            st.info(
                "No numerical columns are available "
                "for statistical analysis."
            )

        else:

            statistics = numeric.describe().T

            statistics.insert(
                0,
                "Column",
                statistics.index,
            )

            statistics.reset_index(
                drop=True,
                inplace=True,
            )

            st.dataframe(
                statistics,
                use_container_width=True,
                hide_index=True,
            )

    # ======================================================
    # Preview Information
    # ======================================================

    st.divider()

    st.subheader("📌 Dataset Information")

    info1, info2, info3, info4 = st.columns(4)

    with info1:

        st.metric(
            "Total Rows",
            f"{dataset.rows:,}",
        )

    with info2:

        st.metric(
            "Total Columns",
            f"{dataset.columns:,}",
        )

    with info3:

        st.metric(
            "Memory Usage",
            dataset.memory_usage,
        )

    with info4:

        st.metric(
            "Health Score",
            f"{dataset.health_score}/100",
        )

    # ======================================================
    # Current Preview Information
    # ======================================================

    st.caption(
        f"Showing {len(preview):,} columns from the uploaded dataset."
    )

    # ======================================================
    # Download
    # ======================================================

    _download_preview(preview)