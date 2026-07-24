"""
constants.py

This module contains application-wide constants used throughout
ML Studio. Only values that remain constant during runtime
should be defined here.
"""

from typing import Final


# ==========================================================
# Application
# ==========================================================

APP_NAME: Final[str] = "ML Studio"
APP_VERSION: Final[str] = "1.0.0"

APP_ICON: Final[str] = "🤖"


# ==========================================================
# Navigation
# ==========================================================

PAGES: Final[tuple[str, ...]] = (
    "Dashboard",
    "Dataset",
    "Preprocessing",
    "Feature Engineering",
    "Model Training",
    "Prediction",
    "Reports",
    "Settings",
)


# ==========================================================
# Dataset
# ==========================================================

SUPPORTED_FILE_TYPES: Final[tuple[str, ...]] = (
    "csv",
    "xlsx",
    "xls",
)

DEFAULT_RANDOM_STATE: Final[int] = 42


# ==========================================================
# Machine Learning
# ==========================================================

PROBLEM_TYPES: Final[tuple[str, ...]] = (
    "Classification",
    "Regression",
    "Clustering",
)


# ==========================================================
# Workflow
# ==========================================================

WORKFLOW_STAGES: Final[tuple[str, ...]] = (
    "Dataset",
    "Preprocessing",
    "Feature Engineering",
    "Model Training",
    "Prediction",
    "Reports",
)


# ==========================================================
# Theme
# ==========================================================

PRIMARY_COLOR: Final[str] = "#2563EB"
SUCCESS_COLOR: Final[str] = "#16A34A"
WARNING_COLOR: Final[str] = "#F59E0B"
ERROR_COLOR: Final[str] = "#DC2626"
INFO_COLOR: Final[str] = "#0EA5E9"