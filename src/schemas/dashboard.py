"""
dashboard.py

Purpose:
    Dashboard data models.

Author:
    Shahid

Project:
    ML Studio
"""

from dataclasses import dataclass
from typing import Any


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
class QuickAction:
    """
    Dashboard quick action.
    """

    label: str
    icon: str
    page: str
    enabled: bool


@dataclass
class DashboardData:
    """
    Dashboard information.
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

    primary_action: QuickAction
    secondary_actions: list[QuickAction]