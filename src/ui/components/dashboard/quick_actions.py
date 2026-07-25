"""
quick_actions.py

Dashboard quick actions.
"""

import streamlit as st

from src.schemas.dashboard import QuickAction


def render_quick_actions(
    primary_action: QuickAction,
    secondary_actions: list[QuickAction],
) -> None:

    st.subheader("Quick Actions")

    if st.button(
        f"{primary_action.icon} {primary_action.label}",
        disabled=not primary_action.enabled,
        use_container_width=True,
    ):
        st.switch_page(primary_action.page)

    st.write("")

    cols = st.columns(len(secondary_actions))

    for col, action in zip(cols, secondary_actions):

        with col:

            if st.button(
                f"{action.icon} {action.label}",
                disabled=not action.enabled,
                use_container_width=True,
                key=action.label,
            ):

                if action.page:
                    st.switch_page(action.page)

    st.divider()