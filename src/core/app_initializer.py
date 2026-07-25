"""
Application initialization.
"""

import streamlit as st

from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager
from src.ui.sidebar import render_sidebar
from src.ui.theme import apply_theme


def initialize_page() -> None:
    """
    Initialize every ML Studio page.
    """

    st.set_page_config(
        page_title="ML Studio",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_theme()

    SessionManager.initialize()
    WorkflowManager.initialize()
    PipelineManager.initialize()
    HistoryManager.initialize()

    render_sidebar()