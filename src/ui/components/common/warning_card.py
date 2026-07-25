"""
warning_card.py

Purpose:
    Warning card component.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_warning_card(
    title: str,
    message: str,
) -> None:
    """
    Render warning card.
    """

    st.markdown(
        f"""
<div style="
padding:18px;
border-left:6px solid #F59E0B;
background:#FFF7ED;
border-radius:10px;
margin-bottom:12px;
">

<h4 style="margin:0;">
⚠️ {title}
</h4>

<p style="margin-top:8px;margin-bottom:0;">
{message}
</p>

</div>
""",
        unsafe_allow_html=True,
    )