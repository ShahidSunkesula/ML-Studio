"""
dataset_service.py

Purpose:
    Handles dataset upload and provides dataset information
    for the Dataset page.

Author:
    Shahid

Project:
    ML Studio
"""

from pathlib import Path

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
from src.schemas.dataset import DatasetData


class DatasetService:
    """
    Service responsible for dataset operations.
    """

    # ======================================================
    # Upload Dataset
    # ======================================================

    @staticmethod
    def upload_dataset(uploaded_file) -> bool:
        """
        Upload dataset and update application state.
        """

        if uploaded_file is None:
            return False

        try:

            # --------------------------------------------------
            # Read Dataset
            # --------------------------------------------------

            if uploaded_file.name.lower().endswith(".csv"):

                dataset = pd.read_csv(uploaded_file)

            elif uploaded_file.name.lower().endswith(".xlsx"):

                dataset = pd.read_excel(uploaded_file)

            else:
                return False

            if dataset.empty:
                return False

            # --------------------------------------------------
            # Store Dataset
            # --------------------------------------------------

            SessionManager.set("dataset", dataset)
            SessionManager.set("dataset_name", uploaded_file.name)

            # File size (MB)

            uploaded_file.seek(0, 2)
            file_size = uploaded_file.tell() / (1024 ** 2)
            uploaded_file.seek(0)

            SessionManager.set(
                "dataset_file_size",
                f"{file_size:.2f} MB",
            )

            # --------------------------------------------------
            # Workflow
            # --------------------------------------------------

            WorkflowManager.complete("dataset_uploaded")

            # --------------------------------------------------
            # Pipeline
            # --------------------------------------------------

            PipelineManager.add_step(
                step="Dataset Upload",
                method="File Upload",
                parameters={
                    "filename": uploaded_file.name,
                    "rows": len(dataset),
                    "columns": len(dataset.columns),
                },
            )

            # --------------------------------------------------
            # History
            # --------------------------------------------------

            HistoryManager.add_event(
                action="Dataset Uploaded",
                details={
                    "filename": uploaded_file.name,
                    "rows": len(dataset),
                    "columns": len(dataset.columns),
                },
            )

            return True

        except Exception as e:

            print(e)
            return False

    # ======================================================
    # Dataset Information
    # ======================================================

    @staticmethod
    def get_dataset_data() -> DatasetData:
        """
        Return dataset information for rendering.
        """

        dataset = SessionManager.get("dataset")
        dataset_name = SessionManager.get("dataset_name")
        file_size = SessionManager.get("dataset_file_size", "0 MB")

        # --------------------------------------------------
        # No Dataset
        # --------------------------------------------------

        if dataset is None:

            return DatasetData(
                dataset_name=None,
                file_type="-",
                file_size="0 MB",
                rows=0,
                columns=0,
                numeric_columns=0,
                categorical_columns=0,
                boolean_columns=0,
                datetime_columns=0,
                missing_values=0,
                missing_percentage=0,
                duplicate_rows=0,
                duplicate_percentage=0,
                constant_columns=0,
                high_cardinality_columns=0,
                empty_columns=0,
                memory_usage="0 MB",
                health_score=0,
                health_status="No Dataset",
                preview=None,
                column_summary=None,
                upload_status=False,
                upload_message="No dataset uploaded.",
            )

        # ======================================================
        # Basic Information
        # ======================================================

        rows = len(dataset)
        columns = len(dataset.columns)

        file_type = Path(dataset_name).suffix.upper().replace(".", "")

        memory_usage = (
            f"{dataset.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB"
        )

        # ======================================================
        # Column Types
        # ======================================================

        numeric_columns = sum(
            is_numeric_dtype(dataset[col])
            for col in dataset.columns
        )

        categorical_columns = sum(
            dataset[col].dtype == "object"
            for col in dataset.columns
        )

        boolean_columns = sum(
            is_bool_dtype(dataset[col])
            for col in dataset.columns
        )

        datetime_columns = sum(
            is_datetime64_any_dtype(dataset[col])
            for col in dataset.columns
        )

        # ======================================================
        # Missing Values
        # ======================================================

        missing_values = int(dataset.isna().sum().sum())

        total_cells = rows * columns

        missing_percentage = (
            (missing_values / total_cells) * 100
            if total_cells
            else 0
        )

        # ======================================================
        # Duplicate Rows
        # ======================================================

        duplicate_rows = int(dataset.duplicated().sum())

        duplicate_percentage = (
            (duplicate_rows / rows) * 100
            if rows
            else 0
        )

        # ======================================================
        # Constant Columns
        # ======================================================

        constant_columns = sum(
            dataset[col].nunique(dropna=False) <= 1
            for col in dataset.columns
        )

        # ======================================================
        # High Cardinality
        # ======================================================

        high_cardinality_columns = sum(
            dataset[col].nunique() > 0.90 * rows
            for col in dataset.columns
        )

        # ======================================================
        # Empty Columns
        # ======================================================

        empty_columns = sum(
            dataset[col].isna().all()
            for col in dataset.columns
        )

        # ======================================================
        # Dataset Health Score
        # ======================================================

        score = 100

        score -= min(25, missing_percentage * 0.5)
        score -= min(20, duplicate_percentage)
        score -= constant_columns * 3
        score -= empty_columns * 5

        score = max(0, round(score))

        if score >= 90:
            health_status = "Excellent"

        elif score >= 75:
            health_status = "Good"

        elif score >= 50:
            health_status = "Fair"

        else:
            health_status = "Poor"

        # ======================================================
        # Column Summary
        # ======================================================

        column_summary = pd.DataFrame(
            {
                "Column": dataset.columns,
                "Data Type": dataset.dtypes.astype(str),
                "Missing": dataset.isna().sum().values,
                "Missing %": (
                    dataset.isna().sum().values / rows * 100
                ).round(2),
                "Unique": dataset.nunique().values,
            }
        )

        # ======================================================
        # Return
        # ======================================================

        return DatasetData(
            dataset_name=dataset_name,
            file_type=file_type,
            file_size=file_size,
            rows=rows,
            columns=columns,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            boolean_columns=boolean_columns,
            datetime_columns=datetime_columns,
            missing_values=missing_values,
            missing_percentage=round(missing_percentage, 2),
            duplicate_rows=duplicate_rows,
            duplicate_percentage=round(duplicate_percentage, 2),
            constant_columns=constant_columns,
            high_cardinality_columns=high_cardinality_columns,
            empty_columns=empty_columns,
            memory_usage=memory_usage,
            health_score=score,
            health_status=health_status,
            preview=dataset.head(10),
            column_summary=column_summary,
            upload_status=True,
            upload_message="Dataset uploaded successfully.",
        )