"""
empty_state.py

Purpose:
    Empty state component.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_empty_state(
    title: str,
    message: str,
    icon: str = "📂",
):
    """
    Render empty state.
    """

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
<div style="
padding:40px;
text-align:center;
border:2px dashed #CBD5E1;
border-radius:15px;
">

<div style="font-size:60px;">
{icon}
</div>

<h3>
{title}
</h3>

<p style="color:gray;">
{message}
</p>

</div>
""",
        unsafe_allow_html=True,
    )