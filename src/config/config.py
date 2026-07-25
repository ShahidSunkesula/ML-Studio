"""
config.py

Purpose:
    Stores application configuration used across ML Studio.
    These values control application behaviour but are not
    expected to change during runtime.

Author:
    Shahid

Project:
    ML Studio
"""

from pathlib import Path
from typing import Final


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]

ASSETS_DIR: Final[Path] = PROJECT_ROOT / "assets"

DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final[Path] = DATA_DIR / "processed"
SAMPLE_DATA_DIR: Final[Path] = DATA_DIR / "sample"

MODELS_DIR: Final[Path] = PROJECT_ROOT / "models"

REPORTS_DIR: Final[Path] = PROJECT_ROOT / "reports"

TESTS_DIR: Final[Path] = PROJECT_ROOT / "tests"


# ==========================================================
# Dataset Configuration
# ==========================================================

DEFAULT_TEST_SIZE: Final[float] = 0.20

DEFAULT_VALIDATION_SIZE: Final[float] = 0.20

DEFAULT_RANDOM_STATE: Final[int] = 42


# ==========================================================
# Application Configuration
# ==========================================================

MAX_FILE_SIZE_MB: Final[int] = 200

DEFAULT_DECIMAL_PLACES: Final[int] = 2

MAX_PREVIEW_ROWS: Final[int] = 10
