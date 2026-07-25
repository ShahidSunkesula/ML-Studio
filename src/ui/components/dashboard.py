"""
dashboard.py

Reusable dashboard UI components.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.services.dashboard_service import DashboardData
from src.ui.components.metrics import render_metric_card


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


def render_quick_actions(dashboard: DashboardData) -> None:
    """
    Render dashboard quick action buttons.
    """

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

    st.divider()


def render_dataset_summary(dashboard: DashboardData) -> None:
    """
    Render dataset summary information.
    """

    st.subheader("Dataset Summary")

    summary = dashboard.dataset_summary

    if summary.name is None:
        st.info("No dataset has been uploaded yet.")
        st.divider()
        return

    st.write(f"**Dataset:** {summary.name}")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card(
            label="Rows",
            value=f"{summary.rows:,}",
        )

    with col2:
        render_metric_card(
            label="Columns",
            value=summary.columns,
        )

    with col3:
        render_metric_card(
            label="Missing",
            value=f"{summary.missing_values:,}",
        )

    col4, col5 = st.columns(2)

    with col4:
        render_metric_card(
            label="Duplicates",
            value=f"{summary.duplicate_rows:,}",
        )

    with col5:
        render_metric_card(
            label="Memory",
            value=summary.memory_usage,
        )

    st.divider()


def render_workflow_progress(dashboard: DashboardData) -> None:
    """
    Render workflow progress.
    """

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

    st.divider()


def render_pipeline_summary(dashboard: DashboardData) -> None:
    """
    Render completed pipeline steps.
    """

    st.subheader("Pipeline Summary")

    if dashboard.pipeline_step_count == 0:
        st.info("No pipeline steps completed yet.")
        st.divider()
        return

    for step in dashboard.pipeline_steps:

        with st.container(border=True):

            st.write(f"### {step.get('step', 'Unknown Step')}")

            if step.get("method"):
                st.caption(f"Method: {step['method']}")

            if step.get("status"):
                st.caption(f"Status: {step['status']}")

    st.divider()


def render_recent_activity(dashboard: DashboardData) -> None:
    """
    Render recent activity.
    """

    st.subheader("Recent Activity")

    if dashboard.recent_activity_count == 0:
        st.info("No recent activity.")
        return

    for activity in reversed(dashboard.recent_history):

        with st.container(border=True):

            st.write(f"🟢 {activity.get('action', 'Unknown Activity')}")

            if activity.get("details"):
                st.caption(activity["details"])

            if activity.get("timestamp"):
                st.caption(activity["timestamp"])