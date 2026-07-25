"""
metric_card.py

Purpose:
    Reusable metric card component for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from typing import Any

import streamlit as st


def render_metric_card(
    label: str,
    value: Any,
    delta: str | None = None,
    help_text: str | None = None,
) -> None:
    """
    Render a reusable metric card.
    """

    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text,
    )