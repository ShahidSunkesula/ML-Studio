"""
summary.py

Purpose:
    Display detailed information about the selected target.

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
# Target Summary
# ==========================================================


def render_target_summary() -> None:
    """
    Render detailed summary of the selected target.

    Classification:
        - Unique classes
        - Class counts
        - Class percentages
        - Class balance
        - Distribution chart

    Regression:
        - Mean
        - Median
        - Standard deviation
        - Minimum
        - Maximum
        - Distribution chart
    """

    # ======================================================
    # Section Header
    # ======================================================

    render_section_header(
        title="Target Summary",
        subtitle=(
            "Detailed statistics and distribution of "
            "the selected target variable."
        ),
        icon="📊",
    )

    # ======================================================
    # Selected Target Check
    # ======================================================

    target_column = TargetService.get_selected_target()

    if not target_column:

        render_empty_state(
            title="No Target Selected",
            message=(
                "Select and save a target variable "
                "to view its summary."
            ),
            icon="🎯",
        )

        return

    # ======================================================
    # Analyze Target
    # ======================================================

    target_data = TargetService.analyze_target(
        target_column
    )

    if not target_data.selection_status:

        st.error(
            target_data.selection_message
        )

        return

    summary = target_data.summary
    distribution = target_data.distribution
    recommendation = target_data.recommendation

    # ======================================================
    # Target Information
    # ======================================================

    st.subheader("🎯 Target Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Target",
            summary.column,
        )

    with col2:

        st.metric(
            "Data Type",
            summary.data_type,
        )

    with col3:

        st.metric(
            "Unique Values",
            f"{summary.unique_values:,}",
        )

    with col4:

        st.metric(
            "Problem Type",
            target_data.problem_type,
        )

    # ======================================================
    # Target Quality
    # ======================================================

    st.divider()

    st.subheader("✅ Target Quality")

    quality1, quality2, quality3 = st.columns(3)

    with quality1:

        st.metric(
            "Total Rows",
            f"{summary.rows:,}",
        )

    with quality2:

        st.metric(
            "Missing Values",
            f"{summary.missing_values:,}",
        )

    with quality3:

        st.metric(
            "Missing Percentage",
            f"{summary.missing_percentage:.2f}%",
        )

    # ======================================================
    # Missing Value Status
    # ======================================================

    if summary.missing_values == 0:

        st.success(
            "✅ No missing values found in the target."
        )

    else:

        st.warning(
            f"⚠️ The target contains "
            f"{summary.missing_values:,} missing value(s). "
            "These should be handled before model training."
        )

    # ======================================================
    # Target Assessment
    # ======================================================

    st.divider()

    st.subheader("💡 Target Assessment")

    if recommendation.status == "success":

        st.success(
            f"✅ {recommendation.message}"
        )

    elif recommendation.status == "warning":

        st.warning(
            f"⚠️ {recommendation.message}"
        )

    else:

        st.error(
            f"❌ {recommendation.message}"
        )

    # ======================================================
    # Target Distribution
    # ======================================================

    st.divider()

    st.subheader("📈 Target Distribution")

    if (
        distribution.values is None
        or distribution.values.empty
    ):

        st.info(
            "No distribution information is available."
        )

        return

    distribution_df = distribution.values.copy()

    # ======================================================
    # CLASSIFICATION
    # ======================================================

    if distribution.is_classification:

        st.caption(
            "Distribution of the target classes."
        )

        # --------------------------------------------------
        # Class Distribution Table
        # --------------------------------------------------

        st.dataframe(
            distribution_df,
            use_container_width=True,
            hide_index=True,
        )

        # --------------------------------------------------
        # Class Distribution Chart
        # --------------------------------------------------

        if (
            "Value" in distribution_df.columns
            and "Count" in distribution_df.columns
        ):

            chart_data = (
                distribution_df
                .set_index("Value")["Count"]
            )

            st.bar_chart(
                chart_data,
                use_container_width=True,
            )

        # --------------------------------------------------
        # Class Balance
        # --------------------------------------------------

        st.subheader("⚖️ Class Balance")

        if "Percentage" in distribution_df.columns:

            percentages = (
                distribution_df["Percentage"]
            )

            if not percentages.empty:

                largest_class = percentages.max()
                smallest_class = percentages.min()

                imbalance_difference = (
                    largest_class
                    - smallest_class
                )

                balance1, balance2, balance3 = (
                    st.columns(3)
                )

                with balance1:

                    st.metric(
                        "Largest Class",
                        f"{largest_class:.2f}%",
                    )

                with balance2:

                    st.metric(
                        "Smallest Class",
                        f"{smallest_class:.2f}%",
                    )

                with balance3:

                    st.metric(
                        "Difference",
                        f"{imbalance_difference:.2f}%",
                    )

                # --------------------------------------------------
                # Balance Assessment
                # --------------------------------------------------

                if imbalance_difference >= 40:

                    st.error(
                        "🔴 Significant class imbalance detected."
                    )

                    st.caption(
                        "Consider class weighting or "
                        "appropriate resampling techniques "
                        "during preprocessing."
                    )

                elif imbalance_difference >= 20:

                    st.warning(
                        "🟠 Moderate class imbalance detected."
                    )

                    st.caption(
                        "Review the class distribution "
                        "before model training."
                    )

                else:

                    st.success(
                        "🟢 Target classes appear reasonably balanced."
                    )

        # --------------------------------------------------
        # Number of Classes
        # --------------------------------------------------

        st.caption(
            f"The target contains "
            f"**{summary.unique_values:,} unique class(es)**."
        )

    # ======================================================
    # REGRESSION
    # ======================================================

    else:

        st.caption(
            "Statistical summary of the numerical target."
        )

        # --------------------------------------------------
        # Regression Distribution Table
        # --------------------------------------------------

        st.dataframe(
            distribution_df,
            use_container_width=True,
            hide_index=True,
        )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        dataset = TargetService.get_dataset()

        if dataset is not None:

            target = dataset[target_column]

            numeric_target = pd.to_numeric(
                target,
                errors="coerce",
            ).dropna()

            if not numeric_target.empty:

                st.subheader(
                    "📊 Regression Statistics"
                )

                stat1, stat2, stat3, stat4 = (
                    st.columns(4)
                )

                with stat1:

                    st.metric(
                        "Mean",
                        f"{numeric_target.mean():,.4f}",
                    )

                with stat2:

                    st.metric(
                        "Median",
                        f"{numeric_target.median():,.4f}",
                    )

                with stat3:

                    st.metric(
                        "Std Dev",
                        f"{numeric_target.std():,.4f}",
                    )

                with stat4:

                    st.metric(
                        "Minimum",
                        f"{numeric_target.min():,.4f}",
                    )

                stat5, stat6 = st.columns(2)

                with stat5:

                    st.metric(
                        "Maximum",
                        f"{numeric_target.max():,.4f}",
                    )

                with stat6:

                    st.metric(
                        "Non-Missing Values",
                        f"{numeric_target.count():,}",
                    )

                # --------------------------------------------------
                # Regression Distribution
                # --------------------------------------------------

                st.subheader(
                    "📈 Value Distribution"
                )

                st.bar_chart(
                    numeric_target
                    .value_counts()
                    .sort_index()
                    .head(100),
                    use_container_width=True,
                )

    # ======================================================
    # Target Values
    # ======================================================

    st.divider()

    with st.expander(
        "👀 Target Values",
        expanded=False,
    ):

        dataset = TargetService.get_dataset()

        if dataset is None:

            st.info(
                "No dataset available."
            )

        else:

            target = dataset[target_column]

            # ==================================================
            # Classification
            # ==================================================

            if distribution.is_classification:

                unique_values = (
                    target
                    .dropna()
                    .unique()
                )

                unique_df = pd.DataFrame(
                    {
                        target_column: unique_values
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

            else:

                target_preview = (
                    pd.to_numeric(
                        target,
                        errors="coerce",
                    )
                    .dropna()
                    .head(20)
                    .to_frame(
                        name=target_column
                    )
                )

                st.caption(
                    "Showing the first 20 non-missing "
                    "target values."
                )

                st.dataframe(
                    target_preview,
                    use_container_width=True,
                    hide_index=True,
                )