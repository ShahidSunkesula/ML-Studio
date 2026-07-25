"""
summary.py

Purpose:
    Dataset summary component.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.schemas.dataset import DatasetData
from src.ui.components.common import render_metric_card

# ==========================================================
# Helper Functions
# ==========================================================


def _show_health_badge(score: int) -> None:
    """
    Display dataset health badge.
    """

    if score >= 90:
        st.success("🟢 Excellent Dataset")

    elif score >= 75:
        st.success("🟡 Good Dataset")

    elif score >= 50:
        st.warning("🟠 Fair Dataset")

    else:
        st.error("🔴 Poor Dataset")


def _generate_recommendations(dataset: DatasetData) -> list[str]:
    """
    Generate recommendations based on dataset quality.
    """

    recommendations = []

    if dataset.missing_values > 0:
        recommendations.append(
            f"Handle {dataset.missing_values:,} missing values."
        )

    if dataset.duplicate_rows > 0:
        recommendations.append(
            f"Remove {dataset.duplicate_rows:,} duplicate rows."
        )

    if dataset.constant_columns > 0:
        recommendations.append(
            f"Remove {dataset.constant_columns} constant column(s)."
        )

    if dataset.empty_columns > 0:
        recommendations.append(
            f"Remove {dataset.empty_columns} empty column(s)."
        )

    if dataset.high_cardinality_columns > 0:
        recommendations.append(
            "Review high-cardinality categorical columns."
        )

    if not recommendations:
        recommendations.append(
            "Dataset looks clean and is ready for preprocessing."
        )

    return recommendations


# ==========================================================
# Dataset Summary
# ==========================================================


def render_dataset_summary(dataset: DatasetData) -> None:
    """
    Render dataset summary.
    """

    # ======================================================
    # No Dataset
    # ======================================================

    if not dataset.upload_status:
        st.info(dataset.upload_message)
        return

    # ======================================================
    # Header
    # ======================================================

    st.title("📊 Dataset Summary")
    st.caption(
        "Overview of the uploaded dataset before preprocessing."
    )

    st.divider()

    # ======================================================
    # Tabs
    # ======================================================

    summary_tab, quality_tab, health_tab = st.tabs(
        [
            "📁 Summary",
            "✅ Data Quality",
            "❤️ Health",
        ]
    )

    # ======================================================
    # SUMMARY TAB
    # ======================================================

    with summary_tab:

        st.subheader("Dataset Information")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Dataset",
                dataset.dataset_name,
            )

        with c2:
            st.metric(
                "File Type",
                dataset.file_type,
            )

        with c3:
            st.metric(
                "File Size",
                dataset.file_size,
            )

        with c4:
            st.metric(
                "Memory",
                dataset.memory_usage,
            )

        st.divider()

        st.subheader("Dataset Shape")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Rows",
                f"{dataset.rows:,}",
            )

        with c2:
            st.metric(
                "Columns",
                f"{dataset.columns:,}",
            )

        st.divider()

        st.subheader("Column Types")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Numeric",
                dataset.numeric_columns,
            )

        with c2:
            st.metric(
                "Categorical",
                dataset.categorical_columns,
            )

        with c3:
            st.metric(
                "Boolean",
                dataset.boolean_columns,
            )

        with c4:
            st.metric(
                "Datetime",
                dataset.datetime_columns,
            )

    # ======================================================
    # DATA QUALITY TAB
    # ======================================================

    with quality_tab:

        st.subheader("Data Quality")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Missing Values",
                f"{dataset.missing_values:,}",
                f"{dataset.missing_percentage:.2f}%",
            )

        with c2:
            st.metric(
                "Duplicate Rows",
                f"{dataset.duplicate_rows:,}",
                f"{dataset.duplicate_percentage:.2f}%",
            )

        with c3:
            st.metric(
                "Empty Columns",
                dataset.empty_columns,
            )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Constant Columns",
                dataset.constant_columns,
            )

        with c2:
            st.metric(
                "High Cardinality",
                dataset.high_cardinality_columns,
            )

        st.divider()

        st.subheader("Recommendations")

        recommendations = _generate_recommendations(dataset)

        for recommendation in recommendations:
            st.info(recommendation)

    # ======================================================
    # HEALTH TAB
    # ======================================================

    with health_tab:

        st.subheader("Dataset Health")

        st.metric(
            "Health Score",
            f"{dataset.health_score}/100",
        )

        st.progress(dataset.health_score / 100)

        _show_health_badge(dataset.health_score)

        st.divider()

        st.subheader("Quick Statistics")

        left, right = st.columns(2)

        with left:

            st.write(
                f"**Missing Values:** {dataset.missing_values:,}"
            )

            st.write(
                f"**Duplicate Rows:** {dataset.duplicate_rows:,}"
            )

            st.write(
                f"**Constant Columns:** {dataset.constant_columns}"
            )

        with right:

            st.write(
                f"**Memory Usage:** {dataset.memory_usage}"
            )

            st.write(
                f"**Rows:** {dataset.rows:,}"
            )

            st.write(
                f"**Columns:** {dataset.columns:,}"
            )

    st.divider()

    # ======================================================
    # Dataset Insights
    # ======================================================
    st.subheader("💡 Dataset Insights")

    insights = []

    if dataset.rows >= 100000:
        insights.append(
            (
                "📈 Large Dataset",
                "Large datasets may increase preprocessing "
                "and training time.",
            )
        )

    if dataset.numeric_columns > dataset.categorical_columns:
        insights.append(
            (
                "🔢 Mostly Numerical",
                "The dataset primarily contains numerical features.",
            )
        )

    elif dataset.categorical_columns > dataset.numeric_columns:
        insights.append(
            (
                "📝 Mostly Categorical",
                "The dataset contains many categorical features.",
            )
        )

    if dataset.datetime_columns > 0:
        insights.append(
            (
                "📅 Datetime Columns",
                f"{dataset.datetime_columns} datetime column(s) detected.",
            )
        )

    if dataset.boolean_columns > 0:
        insights.append(
            (
                "✔ Boolean Columns",
                f"{dataset.boolean_columns} boolean column(s) detected.",
            )
        )

    if dataset.empty_columns == 0:
        insights.append(
            (
                "✅ Empty Columns",
                "No completely empty columns detected.",
            )
        )

    if not insights:

        st.success(
            "No additional insights available."
        )

    else:

        cols = st.columns(2)

        for i, (title, message) in enumerate(insights):

            with cols[i % 2]:

                with st.container(border=True):

                    st.markdown(f"### {title}")

                    st.write(message)

    st.divider()

    # ======================================================
    # Recommendations
    # ======================================================

    st.subheader("🎯 Recommendations")

    recommendations = _generate_recommendations(dataset)

    for recommendation in recommendations:

        with st.container(border=True):

            st.write(f"• {recommendation}")

    st.divider()

    # ======================================================
    # Technical Details
    # ======================================================

    with st.expander(
        "⚙ Technical Details",
        expanded=False,
    ):

        details = {
            "Dataset Name": dataset.dataset_name,
            "File Type": dataset.file_type,
            "File Size": dataset.file_size,
            "Rows": f"{dataset.rows:,}",
            "Columns": dataset.columns,
            "Memory Usage": dataset.memory_usage,
            "Numeric Columns": dataset.numeric_columns,
            "Categorical Columns": dataset.categorical_columns,
            "Boolean Columns": dataset.boolean_columns,
            "Datetime Columns": dataset.datetime_columns,
            "Missing Values": (
                f"{dataset.missing_values:,}"
            ),
            "Missing Percentage": (
                f"{dataset.missing_percentage:.2f}%"
            ),
            "Duplicate Rows": (
                f"{dataset.duplicate_rows:,}"
            ),
            "Duplicate Percentage": (
                f"{dataset.duplicate_percentage:.2f}%"
            ),
            "Constant Columns": (
                dataset.constant_columns
            ),
            "High Cardinality Columns": (
                dataset.high_cardinality_columns
            ),
            "Empty Columns": (
                dataset.empty_columns
            ),
            "Health Score": (
                f"{dataset.health_score}/100"
            ),
            "Health Status": (
                dataset.health_status
            ),
        }

        left, right = st.columns(2)

        items = list(details.items())
        midpoint = (len(items) + 1) // 2

        with left:
            for key, value in items[:midpoint]:
                st.write(f"**{key}:** {value}")

        with right:
            for key, value in items[midpoint:]:
                st.write(f"**{key}:** {value}")

    st.divider()

    # ======================================================
    # Footer
    # ======================================================

    st.caption(
        f"Dataset **{dataset.dataset_name}** contains "
        f"**{dataset.rows:,} rows** and "
        f"**{dataset.columns} columns**. "
        "Review the quality metrics before proceeding to the "
        "Preprocessing module."
    )