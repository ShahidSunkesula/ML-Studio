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

    # ======================================================
    # Default Workflow
    # ======================================================

    DEFAULT_WORKFLOW = {
        "dataset_uploaded": False,
        "target_selected": False,
        "dataset_profiled": False,
        "preprocessing_completed": False,
        "feature_engineering_completed": False,
        "model_trained": False,
        "prediction_completed": False,
        "report_generated": False,
    }

    # ======================================================
    # Initialize
    # ======================================================

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize workflow state.

        Missing workflow stages are added while
        existing progress is preserved.
        """

        workflow = SessionManager.get(
            "workflow",
            {},
        )

        if workflow is None:
            workflow = {}

        # Add any missing stages without
        # destroying existing progress.

        for stage, default_value in cls.DEFAULT_WORKFLOW.items():

            if stage not in workflow:

                workflow[stage] = default_value

        SessionManager.set(
            "workflow",
            workflow,
        )

    # ======================================================
    # Complete Stage
    # ======================================================

    @classmethod
    def complete(
        cls,
        stage: str,
    ) -> None:
        """
        Mark a workflow stage as completed.
        """

        workflow = SessionManager.get(
            "workflow",
            {},
        )

        if stage not in cls.DEFAULT_WORKFLOW:

            return

        workflow[stage] = True

        SessionManager.set(
            "workflow",
            workflow,
        )

    # ======================================================
    # Reset Stage
    # ======================================================

    @classmethod
    def reset_stage(
        cls,
        stage: str,
    ) -> None:
        """
        Mark a workflow stage as incomplete.
        """

        workflow = SessionManager.get(
            "workflow",
            {},
        )

        if stage not in cls.DEFAULT_WORKFLOW:

            return

        workflow[stage] = False

        SessionManager.set(
            "workflow",
            workflow,
        )

    # ======================================================
    # Reset Workflow
    # ======================================================

    @classmethod
    def reset(cls) -> None:
        """
        Reset the complete workflow.
        """

        SessionManager.set(
            "workflow",
            cls.DEFAULT_WORKFLOW.copy(),
        )

    # ======================================================
    # Is Completed
    # ======================================================

    @classmethod
    def is_completed(
        cls,
        stage: str,
    ) -> bool:
        """
        Check whether a workflow stage is completed.
        """

        workflow = SessionManager.get(
            "workflow",
            {},
        )

        return workflow.get(
            stage,
            False,
        )

    # ======================================================
    # Get Workflow
    # ======================================================

    @classmethod
    def get_workflow(cls) -> dict:
        """
        Return the complete workflow state.
        """

        workflow = SessionManager.get(
            "workflow",
            {},
        )

        return workflow

    # ======================================================
    # Get Completion Percentage
    # ======================================================

    @classmethod
    def get_completion_percentage(cls) -> float:
        """
        Calculate overall workflow completion percentage.
        """

        workflow = cls.get_workflow()

        if not workflow:

            return 0.0

        completed = sum(
            bool(value)
            for value in workflow.values()
        )

        total = len(workflow)

        return round(
            (completed / total) * 100,
            2,
        )