"""
dataset.py

Purpose:
    Dataset data models.

Author:
    Shahid

Project:
    ML Studio
"""

from dataclasses import dataclass

import pandas as pd


@dataclass
class DatasetData:
    """
    Container for dataset page information.
    """

    # --------------------------------------------------
    # Dataset Information
    # --------------------------------------------------

    dataset_name: str | None
    file_type: str
    file_size: str

    # --------------------------------------------------
    # Shape
    # --------------------------------------------------

    rows: int
    columns: int

    # --------------------------------------------------
    # Column Types
    # --------------------------------------------------

    numeric_columns: int
    categorical_columns: int
    boolean_columns: int
    datetime_columns: int

    # --------------------------------------------------
    # Quality Metrics
    # --------------------------------------------------

    missing_values: int
    missing_percentage: float

    duplicate_rows: int
    duplicate_percentage: float

    constant_columns: int
    high_cardinality_columns: int
    empty_columns: int

    # --------------------------------------------------
    # Memory
    # --------------------------------------------------

    memory_usage: str

    # --------------------------------------------------
    # Dataset Health
    # --------------------------------------------------

    health_score: int
    health_status: str

    # --------------------------------------------------
    # Tables
    # --------------------------------------------------

    preview: pd.DataFrame | None
    column_summary: pd.DataFrame | None

    # --------------------------------------------------
    # Upload
    # --------------------------------------------------

    upload_status: bool
    upload_message: str