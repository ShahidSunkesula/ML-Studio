"""
upload.py

Dataset upload component.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_upload_section():
    """
    Render dataset upload section.
    """

    st.subheader("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a dataset",
        type=["csv", "xlsx"],
    )

    return uploaded_file