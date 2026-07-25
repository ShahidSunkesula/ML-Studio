"""
metric_card.py

Reusable Metric Card for ML Studio.
"""

import streamlit as st


def render_metric_card(
    title: str,
    value,
    icon: str = "📊",
    description: str = "",
):
    """
    Render a custom metric card.
    """

    st.markdown(
        f"""
        <div style="
            background:#1E293B;
            border:1px solid #334155;
            border-radius:14px;
            padding:18px;
            min-height:135px;
            box-shadow:0 2px 8px rgba(0,0,0,.15);
        ">
            <div style="
                color:#94A3B8;
                font-size:14px;
                margin-bottom:12px;
            ">
                {icon} {title}
            </div>

            <div style="
                color:white;
                font-size:34px;
                font-weight:700;
                line-height:1.2;
            ">
                {value}
            </div>

            <div style="
                margin-top:12px;
                color:#64748B;
                font-size:13px;
            ">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )