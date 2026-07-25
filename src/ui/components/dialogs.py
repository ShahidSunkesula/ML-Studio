"""
dialogs.py

Purpose:
    Reusable dialog components for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


@st.dialog("Confirmation")
def confirmation_dialog(
    title: str,
    message: str,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
) -> bool:
    """
    Display a reusable confirmation dialog.

    Returns
    -------
    bool
        True if confirmed, otherwise False.
    """

    st.subheader(title)

    st.write(message)

    col1, col2 = st.columns(2)

    with col1:
        confirmed = st.button(
            confirm_label,
            use_container_width=True,
        )

    with col2:
        cancelled = st.button(
            cancel_label,
            use_container_width=True,
        )

    if confirmed:
        return True

    if cancelled:
        return False

    return False