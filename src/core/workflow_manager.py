"""
workflow_manager.py

Purpose:
    Manages the application's workflow progression.

Author:
    Shahid

Project:
    ML Studio
"""

from src.core.session_manager import SessionManager


class WorkflowManager:
    """
    Controls the application's workflow progression.
    """

    DEFAULT_WORKFLOW = {
        "dataset_uploaded": False,
        "dataset_profiled": False,
        "preprocessing_completed": False,
        "feature_engineering_completed": False,
        "model_trained": False,
        "prediction_completed": False,
        "report_generated": False,
    }

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize workflow state.
        """
        workflow = SessionManager.get("workflow")

        if not workflow:
            SessionManager.set("workflow", cls.DEFAULT_WORKFLOW.copy())

    @staticmethod
    def complete(stage: str) -> None:
        """
        Mark a workflow stage as completed.
        """
        workflow = SessionManager.get("workflow")

        if stage in workflow:
            workflow[stage] = True

        SessionManager.set("workflow", workflow)

    @staticmethod
    def reset() -> None:
        """
        Reset the workflow.
        """
        SessionManager.set(
            "workflow",
            WorkflowManager.DEFAULT_WORKFLOW.copy()
        )

    @staticmethod
    def is_completed(stage: str) -> bool:
        """
        Check whether a stage has been completed.
        """
        workflow = SessionManager.get("workflow")

        return workflow.get(stage, False)

    @staticmethod
    def get_workflow() -> dict:
        """
        Return the entire workflow.
        """
        return SessionManager.get("workflow")