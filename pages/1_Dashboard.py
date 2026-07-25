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

    #------------Quick Actions---------------

    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "📂 Upload Dataset",
            disabled=not dashboard.quick_actions["upload_dataset"],
            use_container_width=True,
        )

    with col2:
        st.button(
            "🔄 Continue Project",
            disabled=not dashboard.quick_actions["continue_project"],
            use_container_width=True,
        )
    col3, col4 = st.columns(2)

    with col3:
        st.button(
            "📜 View History",
            use_container_width=True,
        )

    with col4:
        st.button(
            "⚙ Settings",
            use_container_width=True,
        )
        
    # ---------- Workflow Progress ----------
    st.subheader("Workflow Progress")

    st.progress(dashboard.workflow_progress / 100)

    st.caption(
        f"{dashboard.completed_steps} of "
        f"{dashboard.total_steps} steps completed "
        f"({dashboard.workflow_progress:.0f}%)"
    )

    for step, completed in dashboard.workflow.items():
        icon = "✅" if completed else "⬜"
        st.write(f"{icon} {step.replace('_', ' ').title()}")

    # -----------Pipeline Summary-------------
    st.subheader("Pipeline Summary")

    if dashboard.pipeline_step_count == 0:
        st.info("No pipeline steps completed yet.")
    else:
        for step in dashboard.pipeline_steps:
            st.write(f"✅ {step.get('step', 'Unknown Step')}"
            )

    # -----------Recent Activity---------------
    
    st.subheader("Recent Activity")

    if dashboard.recent_activity_count == 0:
        st.info("No recent activity.")
    else:
        for activity in reversed(dashboard.recent_history):
            st.write(f"🟢 {activity['action']}")

if __name__ == "__main__":
    main()