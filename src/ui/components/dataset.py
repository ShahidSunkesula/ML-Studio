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


def render_dataset_summary(dataset):
    pass


def render_dataset_preview(dataset):
    pass


def render_column_summary(dataset):
    pass