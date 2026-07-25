"""
1_Dashboard.py

Purpose:
    Home page for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from src.services.dashboard_service import DashboardService
from src.ui.components.dashboard import (
    render_dataset_summary,
    render_pipeline_summary,
    render_project_overview,
    render_quick_actions,
    render_recent_activity,
    render_workflow_progress,
)
from src.ui.layouts.page_layout import (
    PageConfig,
    render_page_layout,
)
from src.core.app_initializer import initialize_page

initialize_page()

def main() -> None:
    """
    Render the Dashboard page.
    """

    render_page_layout(
        PageConfig(
            title="Dashboard",
            description="Overview of your ML Studio project.",
            icon="🏠",
        )
    )

    dashboard = DashboardService.get_dashboard_data()

    render_project_overview(dashboard)

    render_quick_actions(dashboard)

    render_dataset_summary(dashboard)

    render_workflow_progress(dashboard)

    render_pipeline_summary(dashboard)

    render_recent_activity(dashboard)


if __name__ == "__main__":
    main()