"""
info_card.py

Purpose:
    Reusable information card.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_info_card(
    title: str,
    value: str,
    icon: str = "ℹ️",
) -> None:
    """
    Render information card.
    """

    st.markdown(
        f"""
<div style="
padding:16px;
border-radius:12px;
border:1px solid #D1D5DB;
background:#FAFAFA;
text-align:center;
height:110px;
">

<div style="font-size:28px;">
{icon}
</div>

<div style="
font-size:13px;
color:gray;
">
{title}
</div>

<div style="
font-size:18px;
font-weight:bold;
margin-top:8px;
">
{value}
</div>

</div>
""",
        unsafe_allow_html=True,
    )