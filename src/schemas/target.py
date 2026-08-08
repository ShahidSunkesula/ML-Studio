"""
target.py

Purpose:
    Data models for target variable selection.

Author:
    Shahid

Project:
    ML Studio
"""

from dataclasses import dataclass

import pandas as pd


# ==========================================================
# Target Summary
# ==========================================================


@dataclass
class TargetSummary:
    """
    Summary information about the selected target variable.
    """

    column: str | None

    data_type: str | None

    unique_values: int

    missing_values: int

    missing_percentage: float

    rows: int


# ==========================================================
# Target Distribution
# ==========================================================


@dataclass
class TargetDistribution:
    """
    Distribution information for the target variable.
    """

    values: pd.DataFrame | None

    is_classification: bool


# ==========================================================
# Target Recommendation
# ==========================================================


@dataclass
class TargetRecommendation:
    """
    Recommendation regarding the selected target.
    """

    message: str

    status: str


# ==========================================================
# Target Data
# ==========================================================


@dataclass
class TargetData:
    """
    Complete target-selection information.
    """

    summary: TargetSummary

    problem_type: str | None

    distribution: TargetDistribution

    recommendation: TargetRecommendation

    selection_status: bool

    selection_message: str