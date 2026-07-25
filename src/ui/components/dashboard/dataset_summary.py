"""
dataset_summary.py
"""

import streamlit as st

from src.schemas.dashboard import DashboardData
from src.ui.components.metrics import render_metric_card


def render_dataset_summary(dashboard: DashboardData) -> None:

    st.subheader("Dataset Summary")

    summary = dashboard.dataset_summary

    if summary.name is None:

        st.info("No dataset uploaded.")

        st.divider()

        return

    st.write(f"**Dataset:** {summary.name}")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card("Rows", f"{summary.rows:,}")

    with col2:
        render_metric_card("Columns", summary.columns)

    with col3:
        render_metric_card("Missing", f"{summary.missing_values:,}")

    col4, col5 = st.columns(2)

    with col4:
        render_metric_card(
            "Duplicates",
            f"{summary.duplicate_rows:,}",
        )

    with col5:
        render_metric_card(
            "Memory",
            summary.memory_usage,
        )

    st.divider()