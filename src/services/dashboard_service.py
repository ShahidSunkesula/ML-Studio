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
    completed_steps: int
    total_steps: int
    workflow_progress: float

    pipeline: list
    pipeline_step_count: int

    recent_history: list
    recent_activity_count: int

    quick_actions: dict
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

        # -------- Workflow Statistics --------
        workflow = WorkflowManager.get_workflow()

        completed_steps = sum(workflow.values())

        total_steps = len(workflow)

        workflow_progress = (
            (completed_steps / total_steps) * 100
            if total_steps
            else 0
        )

        # -------- get pipeline---------------
        
        pipeline = PipelineManager.get_pipeline()
        pipeline_step_count = len(pipeline)

        # -------- get history----------------
        
        history = HistoryManager.get_history()
        recent_history = history[-5:]
        recent_activity_count = len(recent_history)

        #----------Quick Actions--------------

        quick_actions = {
            "upload_dataset": dataset is None,
            "continue_project": dataset is not None,
            "view_history": True,
            "settings": True,
        }
        # -------- Return Dashboard Data --------
        return DashboardData(
            dataset_name=dataset_name,
            dataset_rows=rows,
            dataset_columns=columns,
            model_count=0,
            workflow=workflow,
            completed_steps=completed_steps,
            total_steps=total_steps,
            workflow_progress=workflow_progress,
            pipeline_steps=pipeline,
            pipeline_step_count=pipeline_step_count,
            recent_history=recent_history,
            recent_activity_count=recent_activity_count,
            quick_actions=quick_actions,
        )