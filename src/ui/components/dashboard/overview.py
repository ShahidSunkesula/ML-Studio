"""
overview.py

Project overview component.
"""

from src.schemas.dashboard import DashboardData
from src.ui.components.metrics import render_metric_card
import streamlit as st


def render_project_overview(dashboard: DashboardData) -> None:
    """
    Render the project overview metrics.
    """

    st.subheader("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            label="Dataset",
            value=dashboard.dataset_summary.name or "None",
        )

    with col2:
        render_metric_card(
            label="Rows",
            value=f"{dashboard.dataset_summary.rows:,}",
        )

    with col3:
        render_metric_card(
            label="Columns",
            value=dashboard.dataset_summary.columns,
        )

    with col4:
        render_metric_card(
            label="Models",
            value=dashboard.model_count,
        )

    st.divider()