"""
dataset_service.py

Purpose:
    Used to Upload data to ML Studio.

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

    dataset_name: str | None

    rows: int

    columns: int

    missing_values: int

    duplicate_rows: int

    memory_usage: str

    preview: pd.DataFrame | None

    column_summary: pd.DataFrame | None

    upload_status: bool
class DatasetService:
    """
    Service responsible for dataset operations.
    """

    @staticmethod
    def get_dataset_data() -> DatasetData:
        """
        Collect all dataset page information.
        """

        pass