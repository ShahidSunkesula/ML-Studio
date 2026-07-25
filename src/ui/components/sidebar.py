"""
sidebar.py

Purpose:
    Renders the application's sidebar.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.core.constants import APP_NAME, APP_VERSION
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager
from src.core.pipeline_manager import PipelineManager
from src.core.history_manager import HistoryManager


def render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    workflow = WorkflowManager.get_workflow()
    pipeline = PipelineManager.get_pipeline()
    history = HistoryManager.get_history()
    dataset = SessionManager.get("dataset")

    completed_steps = sum(workflow.values())
    total_steps = len(workflow)

    with st.sidebar:

        st.title(APP_NAME)
        st.caption(f"Version {APP_VERSION}")

        st.divider()

        st.subheader("Workflow")

        st.progress(completed_steps / total_steps)

        st.write(
            f"Completed: {completed_steps}/{total_steps}"
        )

        st.divider()

        st.subheader("Project")

        if dataset is None:
            st.info("No dataset loaded")
        else:
            st.success("Dataset loaded")

        st.metric(
            "Pipeline Steps",
            len(pipeline)
        )

        st.metric(
            "History Events",
            len(history)
        )

        st.divider()

        st.subheader("Quick Actions")

        st.button(
            "Refresh",
            use_container_width=True,
            disabled=True,
        )

        st.button(
            "Reset Project",
            use_container_width=True,
            disabled=True,
        )