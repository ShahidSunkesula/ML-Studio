"""
app.py

Purpose:
    Entry point for the ML Studio application.

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
from src.core.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(__name__)


# ==========================================================
# Streamlit Page Configuration
# ==========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# Initialize Core Managers
# ==========================================================

SessionManager.initialize()
WorkflowManager.initialize()
PipelineManager.initialize()
HistoryManager.initialize()

logger.info("ML Studio started successfully.")


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:
    st.title(APP_NAME)
    st.caption(f"Version {APP_VERSION}")

    st.divider()

    st.success("Core initialized successfully")

    st.divider()

    st.write("Navigate using the pages on the left.")


# ==========================================================
# Main Page
# ==========================================================

st.title("🧠 ML Studio")

st.subheader("Machine Learning Workflow Platform")

st.write(
    """
Welcome to **ML Studio**.

This application helps you build complete machine learning
pipelines through an interactive workflow.

Use the navigation menu to begin.
"""
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pipeline Steps", len(PipelineManager.get_pipeline()))

with col2:
    st.metric("History Events", len(HistoryManager.get_history()))

with col3:
    workflow = WorkflowManager.get_workflow()
    completed = sum(workflow.values())
    st.metric("Workflow Progress", f"{completed}/{len(workflow)}")