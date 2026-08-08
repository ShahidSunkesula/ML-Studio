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

    # ======================================================
    # Default State
    # ======================================================

    DEFAULT_STATE = {

        # --------------------------------------------------
        # Dataset
        # --------------------------------------------------

        "dataset": None,
        "dataset_name": None,
        "dataset_file_size": "0 MB",
        "last_uploaded_file": None,

        # --------------------------------------------------
        # Target Selection
        # --------------------------------------------------

        "target_column": None,
        "target_selected": False,
        "problem_type": None,
        "target_dtype": None,
        "target_unique_values": 0,
        "target_missing_values": 0,
        "target_classes": [],

        # --------------------------------------------------
        # Pipeline
        # --------------------------------------------------

        "pipeline": [],

        # --------------------------------------------------
        # History
        # --------------------------------------------------

        "history": [],

        # --------------------------------------------------
        # Workflow
        # --------------------------------------------------

        "workflow": {},

        # --------------------------------------------------
        # Models
        # --------------------------------------------------

        "trained_model": None,

        # --------------------------------------------------
        # Prediction
        # --------------------------------------------------

        "prediction": None,

        # --------------------------------------------------
        # Profiling
        # --------------------------------------------------

        "profile": None,

        # --------------------------------------------------
        # Errors
        # --------------------------------------------------

        "target_selection_error": None,
    }

    # ======================================================
    # Initialize
    # ======================================================

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize session state with default values.

        Existing values are preserved.
        """

        for key, value in cls.DEFAULT_STATE.items():

            if key not in st.session_state:

                # Copy mutable defaults so different
                # session-state values do not share
                # the same list/dictionary object.

                if isinstance(value, list):

                    st.session_state[key] = value.copy()

                elif isinstance(value, dict):

                    st.session_state[key] = value.copy()

                else:

                    st.session_state[key] = value

    # ======================================================
    # Get
    # ======================================================

    @staticmethod
    def get(
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Get a value from session state.
        """

        return st.session_state.get(
            key,
            default,
        )

    # ======================================================
    # Set
    # ======================================================

    @staticmethod
    def set(
        key: str,
        value: Any,
    ) -> None:
        """
        Store a value in session state.
        """

        st.session_state[key] = value

    # ======================================================
    # Delete
    # ======================================================

    @staticmethod
    def delete(
        key: str,
    ) -> None:
        """
        Delete a key from session state.
        """

        if key in st.session_state:

            del st.session_state[key]

    # ======================================================
    # Exists
    # ======================================================

    @staticmethod
    def exists(
        key: str,
    ) -> bool:
        """
        Check whether a key exists in session state.
        """

        return key in st.session_state

    # ======================================================
    # Clear
    # ======================================================

    @staticmethod
    def clear() -> None:
        """
        Clear the entire session state.
        """

        st.session_state.clear()

    # ======================================================
    # Reset Dataset
    # ======================================================

    @classmethod
    def reset_dataset_state(cls) -> None:
        """
        Reset dataset-related state.
        """

        dataset_keys = [
            "dataset",
            "dataset_name",
            "dataset_file_size",
            "last_uploaded_file",
        ]

        for key in dataset_keys:

            default = cls.DEFAULT_STATE.get(
                key
            )

            if isinstance(default, list):

                default = default.copy()

            elif isinstance(default, dict):

                default = default.copy()

            st.session_state[key] = default

    # ======================================================
    # Reset Target
    # ======================================================

    @classmethod
    def reset_target_state(cls) -> None:
        """
        Reset target-selection state.
        """

        target_keys = [
            "target_column",
            "target_selected",
            "problem_type",
            "target_dtype",
            "target_unique_values",
            "target_missing_values",
            "target_classes",
            "target_selection_error",
        ]

        for key in target_keys:

            default = cls.DEFAULT_STATE.get(
                key
            )

            if isinstance(default, list):

                default = default.copy()

            elif isinstance(default, dict):

                default = default.copy()

            st.session_state[key] = default

    # ======================================================
    # Reset Profile
    # ======================================================

    @classmethod
    def reset_profile_state(cls) -> None:
        """
        Reset profiling-related state.
        """

        st.session_state["profile"] = None