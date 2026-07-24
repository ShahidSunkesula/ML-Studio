"""
pipeline_manager.py

Purpose:
    Manages the machine learning pipeline by storing every
    processing step applied to the dataset.

Author:
    Shahid

Project:
    ML Studio
"""

from typing import Any

from src.core.session_manager import SessionManager


class PipelineManager:
    """
    Manages the ML processing pipeline.
    """

    PIPELINE_KEY = "pipeline"

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the pipeline.
        """
        if SessionManager.get(cls.PIPELINE_KEY) is None:
            SessionManager.set(cls.PIPELINE_KEY, [])

    @classmethod
    def add_step(
        cls,
        step: str,
        method: str,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """
        Add a processing step to the pipeline.
        """

        pipeline = SessionManager.get(cls.PIPELINE_KEY)

        pipeline.append(
            {
                "step": step,
                "method": method,
                "parameters": parameters or {},
                "status": "Completed",
            }
        )

        SessionManager.set(cls.PIPELINE_KEY, pipeline)

    @classmethod
    def get_pipeline(cls) -> list:
        """
        Return the complete pipeline.
        """
        return SessionManager.get(cls.PIPELINE_KEY)

    @classmethod
    def clear(cls) -> None:
        """
        Clear the pipeline.
        """
        SessionManager.set(cls.PIPELINE_KEY, [])

    @classmethod
    def remove_last_step(cls) -> None:
        """
        Remove the most recently added step.
        """
        pipeline = SessionManager.get(cls.PIPELINE_KEY)

        if pipeline:
            pipeline.pop()

        SessionManager.set(cls.PIPELINE_KEY, pipeline)