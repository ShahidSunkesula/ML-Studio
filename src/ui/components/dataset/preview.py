"""
preview.py

Dataset preview component.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st

from src.services.dataset_service import DatasetData


def render_dataset_preview(dataset: DatasetData):
    """
    Render dataset preview.
    """

    st.subheader("Dataset Preview")

    if dataset.preview is None:

        st.info("No dataset available.")

        st.divider()

        return

    st.dataframe(
        dataset.preview,
        use_container_width=True,
    )

    st.divider()