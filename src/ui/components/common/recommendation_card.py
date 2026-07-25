"""
recommendation_card.py

Purpose:
    Reusable recommendation card.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_recommendation_card(
    title: str,
    message: str,
    severity: str = "info",
) -> None:
    """
    Render recommendation card.

    Parameters
    ----------
    title : str
        Recommendation title.

    message : str
        Recommendation details.

    severity : str
        success | info | warning | error
    """

    colours = {
        "success": "#D1FAE5",
        "info": "#DBEAFE",
        "warning": "#FEF3C7",
        "error": "#FECACA",
    }

    icons = {
        "success": "✅",
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
    }

    colour = colours.get(severity, "#DBEAFE")
    icon = icons.get(severity, "ℹ️")

    st.markdown(
        f"""
<div style="
background:{colour};
padding:18px;
border-radius:12px;
margin-bottom:10px;
">

<h4 style="margin:0;">
{icon} {title}
</h4>

<p style="margin-top:8px;margin-bottom:0;">
{message}
</p>

</div>
""",
        unsafe_allow_html=True,
    )