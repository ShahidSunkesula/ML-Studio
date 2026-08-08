"""
target_service.py

Purpose:
    Handles target variable selection, validation,
    classification/regression detection, and target analysis.

Author:
    Shahid

Project:
    ML Studio
"""

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager
from src.schemas.target import (
    TargetData,
    TargetDistribution,
    TargetRecommendation,
    TargetSummary,
)


class TargetService:
    """
    Service responsible for target variable operations.
    """

    # ======================================================
    # Get Dataset
    # ======================================================

    @staticmethod
    def get_dataset() -> pd.DataFrame | None:
        """
        Return the currently loaded dataset.

        Public method intended for UI components and
        other application services.
        """

        return SessionManager.get("dataset")

    # ======================================================
    # Internal Dataset Access
    # ======================================================

    @staticmethod
    def _get_dataset() -> pd.DataFrame | None:
        """
        Internal compatibility wrapper for dataset access.
        """

        return TargetService.get_dataset()

    # ======================================================
    # Get Available Columns
    # ======================================================

    @staticmethod
    def get_available_columns() -> list[str]:
        """
        Return all columns available for target selection.
        """

        dataset = TargetService.get_dataset()

        if dataset is None:
            return []

        return [
            str(column)
            for column in dataset.columns
        ]

    # ======================================================
    # Detect Problem Type
    # ======================================================

    @staticmethod
    def detect_problem_type(
        dataset: pd.DataFrame,
        target_column: str,
    ) -> str:
        """
        Automatically detect whether the target represents
        regression, binary classification, or multiclass
        classification.

        Returns
        -------
        str
            One of:

            - Regression
            - Binary Classification
            - Multiclass Classification
            - Unknown
        """

        if target_column not in dataset.columns:
            return "Unknown"

        target = dataset[target_column]

        unique_values = target.nunique(
            dropna=True
        )

        # --------------------------------------------------
        # No Useful Values
        # --------------------------------------------------

        if unique_values == 0:
            return "Unknown"

        # --------------------------------------------------
        # Boolean Target
        # --------------------------------------------------

        if is_bool_dtype(target):

            return "Binary Classification"

        # --------------------------------------------------
        # Datetime Target
        # --------------------------------------------------

        if is_datetime64_any_dtype(target):

            return "Unknown"

        # --------------------------------------------------
        # Numeric Target
        # --------------------------------------------------

        if is_numeric_dtype(target):

            # Two unique numeric values
            # normally represent binary classification.

            if unique_values == 2:

                return "Binary Classification"

            # Small discrete integer-like targets
            # are treated as classification.

            if (
                unique_values <= 20
                and TargetService._is_discrete_numeric(
                    target
                )
            ):

                return "Multiclass Classification"

            return "Regression"

        # --------------------------------------------------
        # Categorical / Object Target
        # --------------------------------------------------

        if unique_values == 2:

            return "Binary Classification"

        return "Multiclass Classification"

    # ======================================================
    # Detect Discrete Numeric Target
    # ======================================================

    @staticmethod
    def _is_discrete_numeric(
        target: pd.Series,
    ) -> bool:
        """
        Determine whether a numeric target behaves like
        a discrete variable.
        """

        if target.empty:

            return False

        non_null = target.dropna()

        if non_null.empty:

            return False

        try:

            return bool(
                (non_null % 1 == 0).all()
            )

        except Exception:

            return False

    # ======================================================
    # Build Target Summary
    # ======================================================

    @staticmethod
    def _build_target_summary(
        dataset: pd.DataFrame,
        target_column: str,
    ) -> TargetSummary:
        """
        Build summary information for the selected target.
        """

        target = dataset[target_column]

        rows = len(target)

        missing_values = int(
            target.isna().sum()
        )

        missing_percentage = (
            (missing_values / rows) * 100
            if rows
            else 0
        )

        return TargetSummary(
            column=target_column,
            data_type=str(target.dtype),
            unique_values=int(
                target.nunique(
                    dropna=True
                )
            ),
            missing_values=missing_values,
            missing_percentage=round(
                missing_percentage,
                2,
            ),
            rows=rows,
        )

    # ======================================================
    # Build Distribution
    # ======================================================

    @staticmethod
    def _build_distribution(
        dataset: pd.DataFrame,
        target_column: str,
        problem_type: str,
    ) -> TargetDistribution:
        """
        Build target distribution information.
        """

        target = dataset[target_column]

        is_classification = (
            problem_type
            in [
                "Binary Classification",
                "Multiclass Classification",
            ]
        )

        # ==================================================
        # Classification
        # ==================================================

        if is_classification:

            distribution = (
                target
                .value_counts(
                    dropna=False
                )
                .rename_axis("Value")
                .reset_index(
                    name="Count"
                )
            )

            total = distribution["Count"].sum()

            if total > 0:

                distribution["Percentage"] = (
                    distribution["Count"]
                    / total
                    * 100
                ).round(2)

            else:

                distribution["Percentage"] = 0.0

            return TargetDistribution(
                values=distribution,
                is_classification=True,
            )

        # ==================================================
        # Regression
        # ==================================================

        numeric_target = pd.to_numeric(
            target,
            errors="coerce",
        )

        if numeric_target.dropna().empty:

            return TargetDistribution(
                values=None,
                is_classification=False,
            )

        statistics = (
            numeric_target
            .describe()
            .to_frame(
                name="Value"
            )
            .reset_index()
            .rename(
                columns={
                    "index": "Statistic"
                }
            )
        )

        return TargetDistribution(
            values=statistics,
            is_classification=False,
        )

    # ======================================================
    # Build Recommendation
    # ======================================================

    @staticmethod
    def _build_recommendation(
        dataset: pd.DataFrame,
        target_column: str,
        problem_type: str,
    ) -> TargetRecommendation:
        """
        Generate a recommendation for the selected target.
        """

        target = dataset[target_column]

        missing_values = int(
            target.isna().sum()
        )

        unique_values = int(
            target.nunique(
                dropna=True
            )
        )

        # --------------------------------------------------
        # Completely Empty Target
        # --------------------------------------------------

        if target.isna().all():

            return TargetRecommendation(
                message=(
                    "The selected target contains only "
                    "missing values and cannot be used."
                ),
                status="error",
            )

        # --------------------------------------------------
        # No Unique Values
        # --------------------------------------------------

        if unique_values <= 1:

            return TargetRecommendation(
                message=(
                    "The selected target contains only "
                    "one unique value and cannot be used "
                    "for modeling."
                ),
                status="error",
            )

        # --------------------------------------------------
        # Missing Target Values
        # --------------------------------------------------

        if missing_values > 0:

            return TargetRecommendation(
                message=(
                    f"The target contains "
                    f"{missing_values:,} missing value(s). "
                    "These rows may need to be handled "
                    "before model training."
                ),
                status="warning",
            )

        # --------------------------------------------------
        # Binary Classification
        # --------------------------------------------------

        if problem_type == "Binary Classification":

            return TargetRecommendation(
                message=(
                    f"'{target_column}' is suitable for "
                    "binary classification."
                ),
                status="success",
            )

        # --------------------------------------------------
        # Multiclass Classification
        # --------------------------------------------------

        if problem_type == "Multiclass Classification":

            return TargetRecommendation(
                message=(
                    f"'{target_column}' contains "
                    f"{unique_values} classes and is "
                    "suitable for multiclass classification."
                ),
                status="success",
            )

        # --------------------------------------------------
        # Regression
        # --------------------------------------------------

        if problem_type == "Regression":

            return TargetRecommendation(
                message=(
                    f"'{target_column}' is suitable for "
                    "regression."
                ),
                status="success",
            )

        # --------------------------------------------------
        # Unknown
        # --------------------------------------------------

        return TargetRecommendation(
            message=(
                "The selected target could not be reliably "
                "classified as regression or classification."
            ),
            status="error",
        )

    # ======================================================
    # Validate Target
    # ======================================================

    @staticmethod
    def validate_target(
        target_column: str,
    ) -> tuple[bool, str]:
        """
        Validate whether a target can be selected.
        """

        dataset = TargetService.get_dataset()

        # --------------------------------------------------
        # Dataset Check
        # --------------------------------------------------

        if dataset is None:

            return (
                False,
                "No dataset has been uploaded.",
            )

        # --------------------------------------------------
        # Empty Selection
        # --------------------------------------------------

        if not target_column:

            return (
                False,
                "Please select a target column.",
            )

        # --------------------------------------------------
        # Column Check
        # --------------------------------------------------

        if target_column not in dataset.columns:

            return (
                False,
                "Selected target column does not exist.",
            )

        target = dataset[target_column]

        # --------------------------------------------------
        # Completely Missing Target
        # --------------------------------------------------

        if target.isna().all():

            return (
                False,
                "The selected target contains only "
                "missing values.",
            )

        # --------------------------------------------------
        # Datetime Target
        # --------------------------------------------------

        if is_datetime64_any_dtype(target):

            return (
                False,
                "Datetime columns cannot currently be "
                "used as the target.",
            )

        # --------------------------------------------------
        # Single Unique Value
        # --------------------------------------------------

        if (
            target.nunique(
                dropna=True
            ) <= 1
        ):

            return (
                False,
                "The selected target contains only one "
                "unique value and cannot be used for modeling.",
            )

        return (
            True,
            "Target is valid.",
        )

    # ======================================================
    # Analyze Target
    # ======================================================

    @staticmethod
    def analyze_target(
        target_column: str,
    ) -> TargetData:
        """
        Analyze a selected target column.
        """

        dataset = TargetService.get_dataset()

        # ==================================================
        # No Dataset
        # ==================================================

        if dataset is None:

            return TargetData(
                summary=TargetSummary(
                    column=None,
                    data_type=None,
                    unique_values=0,
                    missing_values=0,
                    missing_percentage=0,
                    rows=0,
                ),
                problem_type=None,
                distribution=TargetDistribution(
                    values=None,
                    is_classification=False,
                ),
                recommendation=TargetRecommendation(
                    message=(
                        "No dataset has been uploaded."
                    ),
                    status="error",
                ),
                selection_status=False,
                selection_message=(
                    "No dataset available."
                ),
            )

        # ==================================================
        # Invalid Target
        # ==================================================

        valid, message = (
            TargetService.validate_target(
                target_column
            )
        )

        if not valid:

            if target_column in dataset.columns:

                target = dataset[
                    target_column
                ]

                data_type = str(
                    target.dtype
                )

                rows = len(
                    dataset
                )

                missing_values = int(
                    target.isna().sum()
                )

                missing_percentage = (
                    (
                        missing_values
                        / rows
                    )
                    * 100
                    if rows
                    else 0
                )

                unique_values = int(
                    target.nunique(
                        dropna=True
                    )
                )

            else:

                data_type = None
                rows = len(dataset)
                missing_values = 0
                missing_percentage = 0
                unique_values = 0

            return TargetData(
                summary=TargetSummary(
                    column=target_column,
                    data_type=data_type,
                    unique_values=unique_values,
                    missing_values=missing_values,
                    missing_percentage=round(
                        missing_percentage,
                        2,
                    ),
                    rows=rows,
                ),
                problem_type=None,
                distribution=TargetDistribution(
                    values=None,
                    is_classification=False,
                ),
                recommendation=TargetRecommendation(
                    message=message,
                    status="error",
                ),
                selection_status=False,
                selection_message=message,
            )

        # ==================================================
        # Detect Problem Type
        # ==================================================

        problem_type = (
            TargetService.detect_problem_type(
                dataset,
                target_column,
            )
        )

        # ==================================================
        # Summary
        # ==================================================

        summary = (
            TargetService._build_target_summary(
                dataset,
                target_column,
            )
        )

        # ==================================================
        # Distribution
        # ==================================================

        distribution = (
            TargetService._build_distribution(
                dataset,
                target_column,
                problem_type,
            )
        )

        # ==================================================
        # Recommendation
        # ==================================================

        recommendation = (
            TargetService._build_recommendation(
                dataset,
                target_column,
                problem_type,
            )
        )

        # ==================================================
        # Return
        # ==================================================

        return TargetData(
            summary=summary,
            problem_type=problem_type,
            distribution=distribution,
            recommendation=recommendation,
            selection_status=True,
            selection_message=(
                "Target analyzed successfully."
            ),
        )

    # ======================================================
    # Select Target
    # ======================================================

    @staticmethod
    def select_target(
        target_column: str,
    ) -> bool:
        """
        Select and persist the target variable.
        """

        dataset = TargetService.get_dataset()

        if dataset is None:

            SessionManager.set(
                "target_selection_error",
                "No dataset has been uploaded.",
            )

            return False

        # --------------------------------------------------
        # Validate
        # --------------------------------------------------

        valid, message = (
            TargetService.validate_target(
                target_column
            )
        )

        if not valid:

            SessionManager.set(
                "target_selection_error",
                message,
            )

            return False

        # --------------------------------------------------
        # Detect Problem Type
        # --------------------------------------------------

        problem_type = (
            TargetService.detect_problem_type(
                dataset,
                target_column,
            )
        )

        if problem_type == "Unknown":

            SessionManager.set(
                "target_selection_error",
                (
                    "The selected target could not be "
                    "reliably classified as regression "
                    "or classification."
                ),
            )

            return False

        target = dataset[
            target_column
        ]

        # ==================================================
        # Store Target Configuration
        # ==================================================

        SessionManager.set(
            "target_column",
            target_column,
        )

        SessionManager.set(
            "problem_type",
            problem_type,
        )

        SessionManager.set(
            "target_dtype",
            str(target.dtype),
        )

        SessionManager.set(
            "target_unique_values",
            int(
                target.nunique(
                    dropna=True
                )
            ),
        )

        SessionManager.set(
            "target_missing_values",
            int(
                target.isna().sum()
            ),
        )

        # ==================================================
        # Classification Classes
        # ==================================================

        if problem_type in [
            "Binary Classification",
            "Multiclass Classification",
        ]:

            classes = [
                str(value)
                for value in (
                    target
                    .dropna()
                    .unique()
                )
            ]

        else:

            classes = []

        SessionManager.set(
            "target_classes",
            classes,
        )

        # ==================================================
        # Target Selected
        # ==================================================

        SessionManager.set(
            "target_selected",
            True,
        )

        SessionManager.delete(
            "target_selection_error"
        )

        # ==================================================
        # Workflow
        # ==================================================

        WorkflowManager.complete(
            "target_selected"
        )

        # ==================================================
        # Pipeline
        # ==================================================

        PipelineManager.add_step(
            step="Target Selection",
            method="Target Variable Selection",
            parameters={
                "target_column": target_column,
                "problem_type": problem_type,
                "data_type": str(
                    target.dtype
                ),
                "unique_values": int(
                    target.nunique(
                        dropna=True
                    )
                ),
            },
        )

        # ==================================================
        # History
        # ==================================================

        HistoryManager.add_event(
            action="Target Selected",
            details={
                "target_column": target_column,
                "problem_type": problem_type,
                "data_type": str(
                    target.dtype
                ),
            },
        )

        return True

    # ======================================================
    # Get Selected Target
    # ======================================================

    @staticmethod
    def get_selected_target() -> str | None:
        """
        Return the currently selected target column.
        """

        return SessionManager.get(
            "target_column"
        )

    # ======================================================
    # Get Problem Type
    # ======================================================

    @staticmethod
    def get_problem_type() -> str | None:
        """
        Return the currently selected problem type.
        """

        return SessionManager.get(
            "problem_type"
        )

    # ======================================================
    # Clear Target
    # ======================================================

    @staticmethod
    def clear_target() -> None:
        """
        Clear the selected target configuration.
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

            default = (
                SessionManager.DEFAULT_STATE.get(
                    key
                )
            )

            if isinstance(
                default,
                list,
            ):

                default = default.copy()

            SessionManager.set(
                key,
                default,
            )

        # ==================================================
        # Workflow
        # ==================================================

        WorkflowManager.reset_stage(
            "target_selected"
        )

        # ==================================================
        # History
        # ==================================================

        HistoryManager.add_event(
            action="Target Selection Cleared",
            details={},
        )