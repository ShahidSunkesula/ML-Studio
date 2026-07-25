"""
status_badge.py

Purpose:
    Dataset/model status badges.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


_STATUS = {
    "excellent": ("🟢", "#D1FAE5"),
    "good": ("🟡", "#FEF3C7"),
    "fair": ("🟠", "#FED7AA"),
    "poor": ("🔴", "#FECACA"),
    "info": ("🔵", "#DBEAFE"),
}


def render_status_badge(status: str) -> None:
    """
    Render coloured status badge.

    Parameters
    ----------
    status : str
    """

    key = status.lower()

    icon, colour = _STATUS.get(
        key,
        ("⚪", "#F3F4F6"),
    )

    st.markdown(
        f"""
<div style="
padding:10px;
border-radius:10px;
background:{colour};
font-weight:600;
text-align:center;
">
{icon} {status.title()}
</div>
""",
        unsafe_allow_html=True,
    )