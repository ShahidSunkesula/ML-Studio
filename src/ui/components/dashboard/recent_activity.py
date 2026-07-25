"""
recent_activity.py
"""

import streamlit as st

from src.schemas.dashboard import DashboardData


def render_recent_activity(dashboard: DashboardData) -> None:

    st.subheader("Recent Activity")

    if dashboard.recent_activity_count == 0:

        st.info("No recent activity.")

        return

    for activity in reversed(dashboard.recent_history):

        with st.container(border=True):

            st.write(f"🟢 {activity.get('action', 'Unknown Activity')}")

            details = activity.get("details")

            if isinstance(details, dict):

                for key, value in details.items():

                    st.caption(f"{key.replace('_', ' ').title()}: {value}")

            elif details:

                st.caption(details)

            if activity.get("timestamp"):

                st.caption(activity["timestamp"])