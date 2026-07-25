"""
dashboard.py

Reusable dashboard UI components.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.services.dashboard_service import (
    DashboardData,
    QuickAction,
)
from src.ui.components.metrics import render_metric_card


# ==========================================================
# Project Overview
# ==========================================================


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


# ==========================================================
# Quick Actions
# ==========================================================


def render_quick_actions(
    primary_action: QuickAction,
    secondary_actions: list[QuickAction],
) -> None:
    """
    Render dashboard quick actions.
    """

    st.subheader("Quick Actions")

    # ---------------- Primary Action ----------------

    if st.button(
        f"{primary_action.icon} {primary_action.label}",
        disabled=not primary_action.enabled,
        use_container_width=True,
    ):
        st.switch_page(primary_action.page)

    st.write("")

    # ---------------- Secondary Actions ----------------

    cols = st.columns(len(secondary_actions))

    for col, action in zip(cols, secondary_actions):

        with col:

            if st.button(
                f"{action.icon} {action.label}",
                disabled=not action.enabled,
                use_container_width=True,
                key=action.label,
            ):
                if action.page:
                    st.switch_page(action.page)

    st.divider()


# ==========================================================
# Dataset Summary
# ==========================================================


def render_dataset_summary(dashboard: DashboardData) -> None:
    """
    Render dataset summary.
    """

    st.subheader("Dataset Summary")

    summary = dashboard.dataset_summary

    if summary.name is None:

        st.info("No dataset uploaded.")

        st.divider()

        return

    st.write(f"**Dataset:** {summary.name}")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card(
            "Rows",
            f"{summary.rows:,}",
        )

    with col2:
        render_metric_card(
            "Columns",
            summary.columns,
        )

    with col3:
        render_metric_card(
            "Missing",
            f"{summary.missing_values:,}",
        )

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


# ==========================================================
# Workflow Progress
# ==========================================================


def render_workflow_progress(dashboard: DashboardData) -> None:
    """
    Render workflow progress.
    """

    st.subheader("Workflow Progress")

    st.progress(dashboard.workflow_progress / 100)

    st.caption(
        f"{dashboard.completed_steps}/{dashboard.total_steps} Steps Completed "
        f"({dashboard.workflow_progress:.0f}%)"
    )

    for step, completed in dashboard.workflow.items():

        icon = "✅" if completed else "⬜"

        st.write(f"{icon} {step.replace('_', ' ').title()}")

    st.divider()


# ==========================================================
# Pipeline Summary
# ==========================================================


def render_pipeline_summary(dashboard: DashboardData) -> None:
    """
    Render pipeline summary.
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


# ==========================================================
# Recent Activity
# ==========================================================


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

            details = activity.get("details")

            if isinstance(details, dict):

                for key, value in details.items():

                    st.caption(f"{key.replace('_', ' ').title()}: {value}")

            elif details:

                st.caption(details)

            if activity.get("timestamp"):

                st.caption(activity["timestamp"])