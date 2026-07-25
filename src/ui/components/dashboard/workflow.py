"""
workflow.py
"""

import streamlit as st

from src.schemas.dashboard import DashboardData


def render_workflow_progress(dashboard: DashboardData) -> None:

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