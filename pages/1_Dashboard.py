"""
1_Dashboard.py

Purpose:
    Home page for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.services.dashboard_service import DashboardService
from src.ui.components.metrics import render_metric_card
from src.ui.layouts.page_layout import (
    PageConfig,
    render_page_layout,
)


def main() -> None:

    render_page_layout(
        PageConfig(
            title="Dashboard",
            description="Overview of your ML Studio project.",
            icon="🏠",
        )
    )

    dashboard = DashboardService.get_dashboard_data()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            label="Dataset",
            value=dashboard.dataset_name or "None",
        )

    with col2:
        render_metric_card(
            label="Rows",
            value=f"{dashboard.dataset_rows:,}",
        )

    with col3:
        render_metric_card(
            label="Columns",
            value=dashboard.dataset_columns,
        )

    with col4:
        render_metric_card(
            label="Models",
            value=dashboard.model_count,
        )


if __name__ == "__main__":
    main()