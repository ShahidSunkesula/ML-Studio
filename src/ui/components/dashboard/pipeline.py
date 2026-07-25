"""
pipeline.py
"""

import streamlit as st

from src.schemas.dashboard import DashboardData


def render_pipeline_summary(dashboard: DashboardData) -> None:

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