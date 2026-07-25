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
from typing import Any

from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager


@dataclass
class DatasetSummary:
    """
    Summary information about the loaded dataset.
    """

    name: str | None
    rows: int
    columns: int
    missing_values: int
    duplicate_rows: int
    memory_usage: str


@dataclass
class DashboardData:
    """
    Container for all dashboard information.
    """

    dataset_summary: DatasetSummary
    model_count: int

    workflow: dict[str, bool]
    completed_steps: int
    total_steps: int
    workflow_progress: float

    pipeline_steps: list[dict[str, Any]]
    pipeline_step_count: int

    recent_history: list[dict[str, Any]]
    recent_activity_count: int

    quick_actions: dict[str, bool]


class DashboardService:
    """
    Service responsible for preparing dashboard data.
    """

    @staticmethod
    def get_dashboard_data() -> DashboardData:
        """
        Collect all dashboard information required by the dashboard page.
        """

        # ---------------- Dataset ----------------

        dataset = SessionManager.get("dataset")
        dataset_name = SessionManager.get("dataset_name")

        if dataset is None:

            dataset_summary = DatasetSummary(
                name=None,
                rows=0,
                columns=0,
                missing_values=0,
                duplicate_rows=0,
                memory_usage="0 MB",
            )

        else:

            dataset_summary = DatasetSummary(
                name=dataset_name,
                rows=len(dataset),
                columns=len(dataset.columns),
                missing_values=int(dataset.isna().sum().sum()),
                duplicate_rows=int(dataset.duplicated().sum()),
                memory_usage=f"{dataset.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            )

        # ---------------- Workflow ----------------

        workflow = WorkflowManager.get_workflow()

        completed_steps = sum(workflow.values())

        total_steps = len(workflow)

        workflow_progress = (
            (completed_steps / total_steps) * 100
            if total_steps > 0
            else 0.0
        )

        # ---------------- Pipeline ----------------

        pipeline_steps = PipelineManager.get_pipeline()

        pipeline_step_count = len(pipeline_steps)

        # ---------------- History ----------------

        history = HistoryManager.get_history()

        recent_history = history[-5:]

        recent_activity_count = len(recent_history)

        # ---------------- Quick Actions ----------------

        quick_actions = {
            "upload_dataset": dataset is None,
            "continue_project": dataset is not None,
            "view_history": True,
            "settings": True,
        }

        # ---------------- Return ----------------

        return DashboardData(
            dataset_summary=dataset_summary,
            model_count=0,
            workflow=workflow,
            completed_steps=completed_steps,
            total_steps=total_steps,
            workflow_progress=workflow_progress,
            pipeline_steps=pipeline_steps,
            pipeline_step_count=pipeline_step_count,
            recent_history=recent_history,
            recent_activity_count=recent_activity_count,
            quick_actions=quick_actions,
        )