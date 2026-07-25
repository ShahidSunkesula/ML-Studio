"""
section_header.py

Purpose:
    Reusable section header.

Author:
    Shahid

Project:
    ML Studio
"""

import streamlit as st


def render_section_header(
    title: str,
    subtitle: str | None = None,
    icon: str = "",
) -> None:
    """
    Render a consistent section header.

    Parameters
    ----------
    title : str
        Section title.

    subtitle : str | None
        Optional subtitle.

    icon : str
        Section icon.
    """

    st.markdown("")

    if subtitle:

        st.markdown(
            f"""
### {icon} {title}

<small style="color:gray;">
{subtitle}
</small>
""",
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"### {icon} {title}"
        )

    st.divider()