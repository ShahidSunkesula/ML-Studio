"""
session_manager.py

Purpose:
    Centralized manager for Streamlit session state.

Author:
    Shahid

Project:
    ML Studio
"""

from typing import Any

import streamlit as st


class SessionManager:
    """
    Manages all application session state.
    """

    DEFAULT_STATE = {
    # Dataset
    "dataset": None,
    "dataset_name": None,
    "last_uploaded_file": None,

    # Project Configuration
    "target_column": None,
    "problem_type": None,

    # Pipeline
    "pipeline": [],

    # History
    "history": [],

    # Workflow
    "workflow": {},

    # Models
    "trained_model": None,
    }

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize session state with default values.
        """
        for key, value in cls.DEFAULT_STATE.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get a value from session state.
        """
        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Store a value in session state.
        """
        st.session_state[key] = value

    @staticmethod
    def delete(key: str) -> None:
        """
        Delete a key from session state.
        """
        if key in st.session_state:
            del st.session_state[key]

    @staticmethod
    def clear() -> None:
        """
        Clear the entire session state.
        """
        st.session_state.clear()