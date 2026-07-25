"""
app.py

Entry point for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.core.app_initializer import initialize_page
from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.workflow_manager import WorkflowManager


def render_home() -> None:
    """
    Render the ML Studio landing page.
    """

    st.title("🧠 ML Studio")

    st.subheader("Machine Learning Workflow Platform")

    st.write(
        """
        Welcome to **ML Studio**.

        This application helps you build complete machine learning
        pipelines through an interactive workflow.

        Use the navigation menu on the left to begin.
        """
    )

    st.divider()

    workflow = WorkflowManager.get_workflow()

    pipeline_steps = PipelineManager.get_pipeline()

    history = HistoryManager.get_history()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Pipeline Steps",
            value=len(pipeline_steps),
        )

    with col2:
        st.metric(
            label="History Events",
            value=len(history),
        )

    with col3:
        st.metric(
            label="Workflow Progress",
            value=f"{sum(workflow.values())}/{len(workflow)}",
        )

    st.divider()

    if st.button(
        "🚀 Open Dashboard",
        use_container_width=True,
    ):
        st.switch_page("pages/1_Dashboard.py")


def main() -> None:
    """
    Application entry point.
    """

    initialize_page()

    render_home()


if __name__ == "__main__":
    main()