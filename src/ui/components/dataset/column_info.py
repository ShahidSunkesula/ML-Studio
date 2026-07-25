"""
column_info.py

Professional Column Summary Component.

Author:
    Shahid

Project:
    ML Studio
"""

import pandas as pd
import streamlit as st

from src.schemas.dataset import DatasetData
from src.ui.components.common import (
    render_empty_state,
    render_section_header,
)


def render_column_summary(dataset: DatasetData) -> None:
    """
    Render dataset column summary.
    """

    render_section_header(
        title="Column Summary",
        subtitle="Inspect dataset features and metadata.",
        icon="🧩",
    )

    if dataset.column_summary is None or dataset.column_summary.empty:

        render_empty_state(
            title="No Column Information",
            message="Upload a dataset to view column details.",
            icon="📋",
        )

        return

    df = dataset.column_summary.copy()

    ##############################################################
    # Search
    ##############################################################

    search = st.text_input(
        "🔍 Search Column",
        placeholder="Enter column name...",
    )

    if search:

        df = df[
            df.iloc[:, 0]
            .astype(str)
            .str.contains(search, case=False)
        ]

    ##############################################################
    # Filters
    ##############################################################

    col1, col2 = st.columns(2)

    with col1:

        if "Data Type" in df.columns:

            dtypes = sorted(df["Data Type"].unique())

            selected = st.multiselect(
                "Filter by Data Type",
                dtypes,
            )

            if selected:

                df = df[df["Data Type"].isin(selected)]

    with col2:

        rows = st.selectbox(
            "Rows",
            [10, 20, 50, 100],
            index=1,
        )

    ##############################################################
    # Metrics
    ##############################################################

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric("Total Columns", dataset.columns)

    with metric2:
        st.metric("Numeric", dataset.numeric_columns)

    with metric3:
        st.metric("Categorical", dataset.categorical_columns)

    with metric4:
        st.metric("Boolean", dataset.boolean_columns)

    st.divider()

    ##############################################################
    # Table
    ##############################################################

    st.dataframe(
        df.head(rows),
        use_container_width=True,
        hide_index=True,
    )

    ##############################################################
    # Download
    ##############################################################

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Column Summary",
        csv,
        "column_summary.csv",
        "text/csv",
        use_container_width=True,
    )

    ##############################################################
    # Quick Insights
    ##############################################################

    st.divider()

    st.subheader("📊 Quick Insights")

    insights = []

    if dataset.numeric_columns > dataset.categorical_columns:
        insights.append(
            "• Dataset contains mostly numerical features."
        )

    if dataset.categorical_columns > dataset.numeric_columns:
        insights.append(
            "• Dataset contains mostly categorical features."
        )

    if dataset.datetime_columns > 0:
        insights.append(
            f"• {dataset.datetime_columns} datetime columns detected."
        )

    if dataset.boolean_columns > 0:
        insights.append(
            f"• {dataset.boolean_columns} boolean columns detected."
        )

    if dataset.high_cardinality_columns > 0:
        insights.append(
            f"• {dataset.high_cardinality_columns} high-cardinality columns found."
        )

    if dataset.constant_columns > 0:
        insights.append(
            f"• {dataset.constant_columns} constant columns detected."
        )

    if not insights:

        st.success("Dataset structure looks healthy.")

    else:

        for item in insights:
            st.markdown(item)