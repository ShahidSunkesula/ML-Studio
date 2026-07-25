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

from dataclasses import dataclass

import pandas as pd

from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager


@dataclass
class DatasetData:
    """
    Container for dataset page information.
    """

    dataset_name: str |None
    rows: int
    columns: int
    missing_values: int
    duplicate_rows: int
    memory_usage: str
    preview: pd.DataFrame | None
    column_summary: pd.DataFrame | None
    upload_status: bool
    upload_message: str


class DatasetService:
    """
    Service responsible for dataset operations.
    """

    @staticmethod
    def upload_dataset(uploaded_file) -> bool:
        """
        Upload a dataset and update application state.
        """

        if uploaded_file is None:
            return False

        try:

            # Read dataset
            if uploaded_file.name.lower().endswith(".csv"):
                dataset = pd.read_csv(uploaded_file)

            elif uploaded_file.name.lower().endswith(".xlsx"):
                dataset = pd.read_excel(uploaded_file)

            else:
                return False

            if dataset.empty:
                return False

            # Store dataset
            SessionManager.set("dataset", dataset)
            SessionManager.set("dataset_name", uploaded_file.name)

            # Update workflow
            WorkflowManager.complete("dataset_uploaded")

            # Update pipeline
            PipelineManager.add_step(
                step="Dataset Upload",
                method="File Upload",
                parameters={
                    "filename": uploaded_file.name,
                    "rows": len(dataset),
                    "columns": len(dataset.columns),
                },
            )

            # Update history
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

    @staticmethod
    def get_dataset_data() -> DatasetData:
        """
        Return dataset information for rendering the Dataset page.
        """

        dataset = SessionManager.get("dataset")
        dataset_name = SessionManager.get("dataset_name")

        if dataset is None:

            return DatasetData(
                dataset_name=None,
                rows=0,
                columns=0,
                missing_values=0,
                duplicate_rows=0,
                memory_usage="0 MB",
                preview=None,
                column_summary=None,
                upload_status=False,
                upload_message="No dataset uploaded.",
            )

        column_summary = pd.DataFrame(
            {
                "Column": dataset.columns,
                "Data Type": dataset.dtypes.astype(str),
                "Missing": dataset.isna().sum().values,
                "Unique": dataset.nunique().values,
            }
        )

        return DatasetData(
            dataset_name=dataset_name,
            rows=len(dataset),
            columns=len(dataset.columns),
            missing_values=int(dataset.isna().sum().sum()),
            duplicate_rows=int(dataset.duplicated().sum()),
            memory_usage=f"{dataset.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB",
            preview=dataset.head(10),
            column_summary=column_summary,
            upload_status=True,
            upload_message="Dataset uploaded successfully.",
        )