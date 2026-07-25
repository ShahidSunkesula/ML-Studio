"""
page_layout.py

Purpose:
    Provides a consistent page layout for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from dataclasses import dataclass

import streamlit as st


@dataclass
class PageConfig:
    """
    Configuration for a page layout.
    """

    title: str
    description: str | None = None
    icon: str | None = None
    show_divider: bool = True


def render_page_layout(config: PageConfig) -> None:
    """
    Render a standardized page layout.

    Parameters
    ----------
    config : PageConfig
        Configuration containing page metadata.
    """

    # ---------- Page Title ----------
    if config.icon:
        st.title(f"{config.icon} {config.title}")
    else:
        st.title(config.title)

    # ---------- Description ----------
    if config.description:
        st.caption(config.description)

    # ---------- Divider ----------
    if config.show_divider:
        st.divider()