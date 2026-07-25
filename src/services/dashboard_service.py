"""
dashboard_service.py

Purpose:
    Provides dashboard data for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from dataclasses import dataclass

from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager


@dataclass
class DashboardData:
    """
    Container for all dashboard information.
    """

    dataset_name: str | None
    dataset_rows: int
    dataset_columns: int
    model_count: int
    workflow: dict
    pipeline: list
    history: list


class DashboardService:
    """
    Service responsible for preparing dashboard data.
    """

    @staticmethod
    def get_dashboard_data() -> DashboardData:
        """
        Collect all dashboard information.
        """

        dataset = SessionManager.get("dataset")
        dataset_name = SessionManager.get("dataset_name")

        rows = 0
        columns = 0

        if dataset is not None:
            rows, columns = dataset.shape

        return DashboardData(
            dataset_name=dataset_name,
            dataset_rows=rows,
            dataset_columns=columns,
            model_count=0,
            workflow=WorkflowManager.get_workflow(),
            pipeline=PipelineManager.get_pipeline(),
            history=HistoryManager.get_history(),
        )