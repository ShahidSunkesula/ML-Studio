"""
dashboard_service.py

Purpose:
    Provides dashboard data for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from src.config.pages import Pages
from src.core.history_manager import HistoryManager
from src.core.pipeline_manager import PipelineManager
from src.core.session_manager import SessionManager
from src.core.workflow_manager import WorkflowManager
from src.schemas.dashboard import (
    DashboardData,
    DatasetSummary,
    QuickAction,
)


class DashboardService:
    """
    Service responsible for preparing dashboard data.
    """

    @staticmethod
    def get_dashboard_data() -> DashboardData:
        """
        Collect dashboard information.
        """

        # ======================================================
        # Dataset
        # ======================================================

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

        # ======================================================
        # Workflow
        # ======================================================

        workflow = WorkflowManager.get_workflow()

        completed_steps = sum(workflow.values())

        total_steps = len(workflow)

        workflow_progress = (
            completed_steps / total_steps * 100
            if total_steps > 0
            else 0.0
        )

        # ======================================================
        # Pipeline
        # ======================================================

        pipeline_steps = PipelineManager.get_pipeline()

        pipeline_step_count = len(pipeline_steps)

        # ======================================================
        # History
        # ======================================================

        history = HistoryManager.get_history()

        recent_history = history[-5:]

        recent_activity_count = len(recent_history)

        # ======================================================
        # Quick Actions
        # ======================================================

        if dataset is None:

            primary_action = QuickAction(
                label="Upload Dataset",
                icon="📂",
                page=Pages.DATASET,
                enabled=True,
            )

        else:

            primary_action = QuickAction(
                label="Open Dataset",
                icon="📂",
                page=Pages.DATASET,
                enabled=True,
            )

        secondary_actions = [
            QuickAction(
                label="History",
                icon="🕘",
                page="",
                enabled=False,
            ),
            QuickAction(
                label="Settings",
                icon="⚙️",
                page="",
                enabled=False,
            ),
        ]

        # ======================================================
        # Return
        # ======================================================

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
            primary_action=primary_action,
            secondary_actions=secondary_actions,
        )