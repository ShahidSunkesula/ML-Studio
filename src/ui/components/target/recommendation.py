"""
recommendation.py

Purpose:
    Display useful ML-specific recommendations and warnings
    for the selected target variable.

Author:
    Shahid

Project:
    ML Studio
"""

import pandas as pd
import streamlit as st

from src.core.session_manager import SessionManager
from src.services.target_service import TargetService
from src.ui.components.common import (
    render_empty_state,
    render_section_header,
)


# ==========================================================
# Helper Functions
# ==========================================================


def _render_check(
    title: str,
    message: str,
    status: str = "info",
) -> None:
    """
    Render a clear recommendation/check card.

    Uses Streamlit's native alert components instead of
    custom recommendation cards so the text remains readable
    in both light and dark themes.
    """

    content = f"**{title}**\n\n{message}"

    if status == "success":

        st.success(content)

    elif status == "warning":

        st.warning(content)

    elif status == "error":

        st.error(content)

    else:

        st.info(content)


# ==========================================================
# Classification Analysis
# ==========================================================


def _classification_recommendations(
    dataset: pd.DataFrame,
    target_column: str,
    problem_type: str,
) -> None:
    """
    Generate recommendations specific to classification targets.
    """

    target = dataset[target_column]

    class_counts = (
        target
        .dropna()
        .value_counts()
    )

    if class_counts.empty:

        _render_check(
            "No Valid Target Classes",
            (
                "The target does not contain usable class "
                "values. Handle the target before continuing."
            ),
            "error",
        )

        return

    # ======================================================
    # Class Overview
    # ======================================================

    st.subheader("🏷️ Class Overview")

    total_classes = len(class_counts)
    total_samples = class_counts.sum()

    largest_class = int(class_counts.max())
    smallest_class = int(class_counts.min())

    largest_class_name = str(
        class_counts.index[0]
    )

    smallest_class_name = str(
        class_counts.index[-1]
    )

    largest_percentage = (
        largest_class / total_samples * 100
    )

    smallest_percentage = (
        smallest_class / total_samples * 100
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Classes",
            total_classes,
        )

    with col2:

        st.metric(
            "Largest Class",
            f"{largest_percentage:.2f}%",
        )

    with col3:

        st.metric(
            "Smallest Class",
            f"{smallest_percentage:.2f}%",
        )

    with col4:

        st.metric(
            "Class Ratio",
            f"{largest_class / max(smallest_class, 1):.1f}:1",
        )

    # ======================================================
    # Class Distribution Table
    # ======================================================

    distribution = pd.DataFrame(
        {
            "Class": class_counts.index.astype(str),
            "Count": class_counts.values,
        }
    )

    distribution["Percentage"] = (
        distribution["Count"]
        / total_samples
        * 100
    ).round(2)

    st.dataframe(
        distribution,
        use_container_width=True,
        hide_index=True,
    )

    # ======================================================
    # Class Balance
    # ======================================================

    imbalance_difference = (
        largest_percentage
        - smallest_percentage
    )

    if imbalance_difference >= 40:

        _render_check(
            "Significant Class Imbalance",
            (
                f"The largest class (**{largest_class_name}**) "
                f"contains {largest_percentage:.2f}% of the "
                f"non-missing target values, while the smallest "
                f"class (**{smallest_class_name}**) contains only "
                f"{smallest_percentage:.2f}%.\n\n"
                "Recommended approach: use stratified train/test "
                "splitting and evaluate models using metrics such "
                "as F1-score, precision, recall, and balanced "
                "accuracy. Consider class weights or resampling "
                "if necessary."
            ),
            "warning",
        )

    elif imbalance_difference >= 20:

        _render_check(
            "Moderate Class Imbalance",
            (
                f"The difference between the largest and smallest "
                f"class is {imbalance_difference:.2f} percentage "
                "points.\n\n"
                "Review the distribution carefully and prefer "
                "stratified splitting during model training."
            ),
            "warning",
        )

    else:

        _render_check(
            "Class Distribution Looks Reasonable",
            (
                f"The difference between the largest and "
                f"smallest classes is only "
                f"{imbalance_difference:.2f} percentage points.\n\n"
                "The target appears reasonably balanced."
            ),
            "success",
        )

    # ======================================================
    # Small Classes
    # ======================================================

    if smallest_class < 10:

        _render_check(
            "Very Small Class Detected",
            (
                f"The smallest class contains only "
                f"{smallest_class} sample(s).\n\n"
                "This can make model training and validation "
                "unreliable. Consider collecting more samples "
                "or reviewing whether this class should be "
                "combined or retained."
            ),
            "warning",
        )

    elif smallest_class < 30:

        _render_check(
            "Small Class Detected",
            (
                f"The smallest class contains only "
                f"{smallest_class} samples.\n\n"
                "Use stratified splitting and check class-level "
                "performance carefully during evaluation."
            ),
            "info",
        )

    # ======================================================
    # Multiclass Specific
    # ======================================================

    if problem_type == "Multiclass Classification":

        if total_classes > 20:

            _render_check(
                "High Number of Classes",
                (
                    f"The target contains {total_classes} classes.\n\n"
                    "Review whether every class has enough "
                    "observations. Multiclass models may become "
                    "more difficult to train and interpret as "
                    "the number of classes increases."
                ),
                "warning",
            )

        else:

            _render_check(
                "Multiclass Target",
                (
                    f"The target contains {total_classes} distinct "
                    "classes.\n\n"
                    "During model training, use a classification "
                    "algorithm that supports multiclass problems "
                    "and evaluate performance for each class."
                ),
                "info",
            )

    # ======================================================
    # Binary Specific
    # ======================================================

    if problem_type == "Binary Classification":

        _render_check(
            "Binary Classification Setup",
            (
                "The target contains exactly two classes.\n\n"
                "For model evaluation, accuracy alone may not "
                "be sufficient when classes are imbalanced. "
                "Also examine precision, recall, F1-score, "
                "ROC-AUC and the confusion matrix."
            ),
            "info",
        )


# ==========================================================
# Regression Analysis
# ==========================================================


def _regression_recommendations(
    dataset: pd.DataFrame,
    target_column: str,
) -> None:
    """
    Generate recommendations specific to regression targets.
    """

    target = pd.to_numeric(
        dataset[target_column],
        errors="coerce",
    ).dropna()

    if target.empty:

        _render_check(
            "No Usable Regression Values",
            (
                "The target does not contain usable numerical "
                "values for regression."
            ),
            "error",
        )

        return

    # ======================================================
    # Basic Statistics
    # ======================================================

    mean = target.mean()
    median = target.median()
    minimum = target.min()
    maximum = target.max()
    std = target.std()

    # ======================================================
    # Regression Overview
    # ======================================================

    st.subheader("📊 Regression Target Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Mean",
            f"{mean:,.3f}",
        )

    with col2:

        st.metric(
            "Median",
            f"{median:,.3f}",
        )

    with col3:

        st.metric(
            "Minimum",
            f"{minimum:,.3f}",
        )

    with col4:

        st.metric(
            "Maximum",
            f"{maximum:,.3f}",
        )

    # ======================================================
    # Skewness
    # ======================================================

    skewness = target.skew()

    if abs(skewness) >= 1:

        _render_check(
            "Highly Skewed Target",
            (
                f"The target has a skewness of "
                f"{skewness:.2f}.\n\n"
                "A strongly skewed target can affect some "
                "regression models. During preprocessing, "
                "inspect the distribution and consider a "
                "suitable transformation such as log or "
                "power transformation when appropriate."
            ),
            "warning",
        )

    elif abs(skewness) >= 0.5:

        _render_check(
            "Moderately Skewed Target",
            (
                f"The target has a skewness of "
                f"{skewness:.2f}.\n\n"
                "Inspect the target distribution during "
                "profiling. A transformation may or may not "
                "be necessary depending on the selected model."
            ),
            "info",
        )

    else:

        _render_check(
            "Target Distribution Looks Reasonable",
            (
                f"The target skewness is {skewness:.2f}.\n\n"
                "There is no strong indication of severe "
                "skewness."
            ),
            "success",
        )

    # ======================================================
    # Outlier Detection
    # ======================================================

    q1 = target.quantile(0.25)
    q3 = target.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = target[
        (target < lower_bound)
        | (target > upper_bound)
    ]

    outlier_percentage = (
        len(outliers)
        / len(target)
        * 100
    )

    if outlier_percentage >= 10:

        _render_check(
            "Many Potential Target Outliers",
            (
                f"Approximately {outlier_percentage:.2f}% of "
                "non-missing target values fall outside the "
                "IQR-based outlier boundaries.\n\n"
                "Inspect these observations during profiling "
                "before deciding whether they are genuine "
                "values or data-quality problems."
            ),
            "warning",
        )

    elif outlier_percentage > 0:

        _render_check(
            "Potential Target Outliers Detected",
            (
                f"Approximately {outlier_percentage:.2f}% of "
                "non-missing target values are outside the "
                "IQR-based boundaries.\n\n"
                "Do not automatically remove them. First "
                "determine whether they represent genuine "
                "observations."
            ),
            "info",
        )

    else:

        _render_check(
            "No IQR-Based Target Outliers",
            (
                "No observations were detected outside the "
                "standard IQR-based boundaries."
            ),
            "success",
        )

    # ======================================================
    # Mean vs Median
    # ======================================================

    if mean != 0:

        mean_median_difference = (
            abs(mean - median)
            / abs(mean)
            * 100
        )

        if mean_median_difference >= 20:

            _render_check(
                "Mean and Median Differ Significantly",
                (
                    f"The mean is {mean:,.3f}, while the median "
                    f"is {median:,.3f}.\n\n"
                    "This may indicate skewness or extreme "
                    "values. Inspect the target distribution "
                    "before selecting the final model."
                ),
                "info",
            )

    # ======================================================
    # Standard Deviation
    # ======================================================

    if std == 0:

        _render_check(
            "Zero Target Variance",
            (
                "The target has no variation. A regression "
                "model cannot learn a useful relationship "
                "from a constant target."
            ),
            "error",
        )


# ==========================================================
# Target Recommendations
# ==========================================================


def render_target_recommendation() -> None:
    """
    Render useful recommendations for the selected target.
    """

    # ======================================================
    # Header
    # ======================================================

    render_section_header(
        title="Target Recommendations",
        subtitle=(
            "Validate your target and understand what "
            "should be checked before preprocessing and "
            "model training."
        ),
        icon="💡",
    )

    # ======================================================
    # Selected Target Check
    # ======================================================

    target_column = (
        TargetService.get_selected_target()
    )

    if not target_column:

        render_empty_state(
            title="No Target Selected",
            message=(
                "Select and save a target variable "
                "to receive recommendations."
            ),
            icon="🎯",
        )

        return

    # ======================================================
    # Dataset
    # ======================================================

    dataset = SessionManager.get("dataset")

    if dataset is None:

        st.error(
            "Dataset is no longer available."
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
    recommendation = target_data.recommendation
    problem_type = target_data.problem_type

    # ======================================================
    # Target Overview
    # ======================================================

    st.subheader("🎯 Target Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Target",
            summary.column,
        )

    with col2:

        st.metric(
            "Problem Type",
            problem_type,
        )

    with col3:

        st.metric(
            "Unique Values",
            f"{summary.unique_values:,}",
        )

    with col4:

        st.metric(
            "Missing Values",
            f"{summary.missing_values:,}",
        )

    # ======================================================
    # Overall Assessment
    # ======================================================

    st.divider()

    st.subheader("🔎 Overall Assessment")

    if recommendation.status == "success":

        _render_check(
            "Target Looks Suitable",
            recommendation.message,
            "success",
        )

    elif recommendation.status == "warning":

        _render_check(
            "Attention Required",
            recommendation.message,
            "warning",
        )

    else:

        _render_check(
            "Target Selection Issue",
            recommendation.message,
            "error",
        )

    # ======================================================
    # Missing Values
    # ======================================================

    if summary.missing_values > 0:

        st.divider()

        _render_check(
            "Missing Target Values",
            (
                f"The target contains "
                f"{summary.missing_values:,} missing value(s), "
                f"which represents "
                f"{summary.missing_percentage:.2f}% of all rows.\n\n"
                "Target values cannot simply be imputed like "
                "ordinary features. ML Studio should handle "
                "these rows separately during preprocessing, "
                "usually by removing rows with missing target "
                "values before model training."
            ),
            "warning",
        )

    else:

        st.divider()

        _render_check(
            "Target Completeness",
            (
                "The selected target contains no missing values. "
                "This is ideal for supervised model training."
            ),
            "success",
        )

    # ======================================================
    # Problem-Specific Analysis
    # ======================================================

    st.divider()

    if problem_type in [
        "Binary Classification",
        "Multiclass Classification",
    ]:

        _classification_recommendations(
            dataset,
            target_column,
            problem_type,
        )

    elif problem_type == "Regression":

        _regression_recommendations(
            dataset,
            target_column,
        )

    else:

        _render_check(
            "Problem Type Could Not Be Determined",
            (
                "Review the target column and make sure it "
                "contains a valid variable suitable for "
                "supervised machine learning."
            ),
            "error",
        )

    # ======================================================
    # Important ML Reminder
    # ======================================================

    st.divider()

    st.subheader("🧠 Important ML Checks")

    _render_check(
        "Avoid Target Leakage",
        (
            "Make sure none of the feature columns contain "
            "information that would only become available "
            "after the target outcome occurs. Target leakage "
            "can produce unrealistically high model scores."
        ),
        "warning",
    )

    _render_check(
        "Keep the Target Out of Features",
        (
            f"'{target_column}' will be used as the prediction "
            "target and should not be included among the input "
            "features during model training."
        ),
        "info",
    )

    # ======================================================
    # Next Step
    # ======================================================

    st.divider()

    st.subheader("🚀 Next Step")

    if problem_type == "Regression":

        st.success(
            "✅ Target selection is complete. "
            "Next: inspect feature distributions, missing "
            "values, outliers, correlations, and feature "
            "types during Data Profiling."
        )

    elif problem_type in [
        "Binary Classification",
        "Multiclass Classification",
    ]:

        st.success(
            "✅ Target selection is complete. "
            "Next: inspect feature distributions, missing "
            "values, categorical features, outliers, "
            "correlations, and class-related patterns during "
            "Data Profiling."
        )

    else:

        st.warning(
            "⚠️ Resolve the target selection issue before "
            "continuing to Data Profiling."
        )