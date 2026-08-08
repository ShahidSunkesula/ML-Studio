"""
selector.py

Purpose:
    Target variable selection component.

Author:
    Shahid

Project:
    ML Studio
"""

import pandas as pd
import streamlit as st

from src.services.target_service import TargetService
from src.ui.components.common import (
    render_empty_state,
    render_section_header,
)


# ==========================================================
# Target Selector
# ==========================================================


def render_target_selector() -> None:
    """
    Render the target variable selection interface.
    """

    # ======================================================
    # Section Header
    # ======================================================

    render_section_header(
        title="Target Variable",
        subtitle=(
            "Select the column you want ML Studio to predict."
        ),
        icon="🎯",
    )

    # ======================================================
    # Dataset Check
    # ======================================================

    columns = TargetService.get_available_columns()

    if not columns:

        render_empty_state(
            title="No Dataset Available",
            message=(
                "Upload a dataset before selecting "
                "a target variable."
            ),
            icon="📂",
        )

        return

    # ======================================================
    # Current Target
    # ======================================================

    current_target = (
        TargetService.get_selected_target()
    )

    # ======================================================
    # Target Selection
    # ======================================================

    default_index = 0

    if current_target in columns:

        default_index = columns.index(
            current_target
        )

    selected_target = st.selectbox(
        "🎯 Target Column",
        options=columns,
        index=default_index,
        key="target_column_selector",
        help=(
            "Choose the column that represents the "
            "value your machine learning model should predict."
        ),
    )

    # ======================================================
    # Get Dataset
    # ======================================================

    dataset = TargetService.get_dataset()

    if dataset is None:

        return

    target_series = dataset[selected_target]

    # ======================================================
    # Analyze Target
    # ======================================================

    target_data = TargetService.analyze_target(
        selected_target
    )

    if not target_data.selection_status:

        st.warning(
            target_data.selection_message
        )

        return

    problem_type = target_data.problem_type

    # ======================================================
    # Target Preview
    # ======================================================

    st.divider()

    st.subheader("Target Preview")

    preview_col1, preview_col2 = st.columns(2)

    # ------------------------------------------------------
    # Data Type
    # ------------------------------------------------------

    with preview_col1:

        st.metric(
            "Data Type",
            str(target_series.dtype),
        )

    # ------------------------------------------------------
    # Unique Values
    # ------------------------------------------------------

    with preview_col2:

        st.metric(
            "Unique Values",
            f"{target_series.nunique(dropna=True):,}",
        )

    # ======================================================
    # Target Values
    # ======================================================

    with st.expander(
        "👀 Target Values",
        expanded=False,
    ):

        # ==================================================
        # Classification
        # ==================================================

        if (
            problem_type
            in [
                "Binary Classification",
                "Multiclass Classification",
            ]
        ):

            unique_values = (
                target_series
                .dropna()
                .unique()
            )

            unique_df = pd.DataFrame(
                {
                    selected_target: unique_values
                }
            )

            st.caption(
                f"Showing all "
                f"{len(unique_values):,} "
                "unique target class(es)."
            )

            st.dataframe(
                unique_df,
                use_container_width=True,
                hide_index=True,
            )

        # ==================================================
        # Regression
        # ==================================================

        elif problem_type == "Regression":

            numeric_target = pd.to_numeric(
                target_series,
                errors="coerce",
            ).dropna()

            preview = (
                numeric_target
                .head(10)
                .to_frame(
                    name=selected_target
                )
            )

            st.caption(
                "Showing the first 10 non-missing "
                "target values."
            )

            st.dataframe(
                preview,
                use_container_width=True,
                hide_index=True,
            )

        # ==================================================
        # Unknown
        # ==================================================

        else:

            st.info(
                "Target values cannot be previewed "
                "until a valid problem type is detected."
            )

    # ======================================================
    # Detected Problem Type
    # ======================================================

    st.divider()

    st.subheader("Detected Problem Type")

    if problem_type == "Regression":

        st.info(
            "📈 Regression\n\n"
            "The selected target appears to represent "
            "a continuous numerical value."
        )

    elif problem_type == "Binary Classification":

        st.info(
            "⚖️ Binary Classification\n\n"
            "The selected target contains two classes."
        )

    elif problem_type == "Multiclass Classification":

        st.info(
            "🏷️ Multiclass Classification\n\n"
            "The selected target contains more than "
            "two classes."
        )

    else:

        st.warning(
            "⚠️ ML Studio could not reliably determine "
            "the problem type."
        )

    # ======================================================
    # Target Quality
    # ======================================================

    st.divider()

    st.subheader("Target Quality")

    quality_col1, quality_col2, quality_col3 = (
        st.columns(3)
    )

    with quality_col1:

        st.metric(
            "Missing Values",
            f"{target_data.summary.missing_values:,}",
        )

    with quality_col2:

        st.metric(
            "Missing %",
            f"{target_data.summary.missing_percentage:.2f}%",
        )

    with quality_col3:

        st.metric(
            "Unique Values",
            f"{target_data.summary.unique_values:,}",
        )

    # ======================================================
    # Save Target
    # ======================================================

    st.divider()

    save_col1, save_col2 = st.columns(
        [2, 1]
    )

    with save_col1:

        st.caption(
            f"Selected target: **{selected_target}**"
        )

    with save_col2:

        if st.button(
            "🎯 Save Target",
            type="primary",
            use_container_width=True,
            key="save_target_button",
        ):

            success = TargetService.select_target(
                selected_target
            )

            if success:

                st.success(
                    f"Target **{selected_target}** "
                    "saved successfully."
                )

                st.rerun()

            else:

                error_message = (
                    st.session_state.get(
                        "target_selection_error",
                        "Unable to save target.",
                    )
                )

                st.error(
                    error_message
                )