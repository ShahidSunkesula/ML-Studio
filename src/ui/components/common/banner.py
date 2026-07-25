"""
banner.py

Purpose:
    Reusable page banner.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_banner(
    title: str,
    subtitle: str = "",
    icon: str = "📊",
) -> None:
    """
    Render page banner.
    """

    st.markdown(
        f"""
<div style="
padding:22px;
border-radius:15px;
background:linear-gradient(135deg,#2563EB,#1D4ED8);
color:white;
margin-bottom:20px;
">

<h2 style="margin:0;">
{icon} {title}
</h2>

<p style="
margin-top:8px;
margin-bottom:0;
font-size:15px;
">
{subtitle}
</p>

</div>
""",
        unsafe_allow_html=True,
    )