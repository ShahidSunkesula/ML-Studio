"""
1_Dashboard.py

Purpose:
    Home page for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from src.core.app_initializer import initialize_page
from src.services.dashboard_service import DashboardService
from src.ui.components.dashboard import (
    render_dataset_summary,
    render_pipeline_summary,
    render_project_overview,
    render_quick_actions,
    render_recent_activity,
    render_workflow_progress,
)
from src.ui.page_layout import (
    PageConfig,
    render_page_layout,
)


# ==========================================================
# Initialize Page
# ==========================================================

initialize_page()


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Render the Dashboard page.
    """

    # ------------------------------------------------------
    # Page Header
    # ------------------------------------------------------

    render_page_layout(
        PageConfig(
            title="Dashboard",
            description="Overview of your ML Studio project.",
            icon="🏠",
        )
    )

    # ------------------------------------------------------
    # Dashboard Data
    # ------------------------------------------------------

    dashboard = DashboardService.get_dashboard_data()

    # ------------------------------------------------------
    # Project Overview
    # ------------------------------------------------------

    render_project_overview(dashboard)

    # ------------------------------------------------------
    # Quick Actions
    # ------------------------------------------------------

    render_quick_actions(
        primary_action=dashboard.primary_action,
        secondary_actions=dashboard.secondary_actions,
    )

    # ------------------------------------------------------
    # Dataset Summary
    # ------------------------------------------------------

    render_dataset_summary(dashboard)

    # ------------------------------------------------------
    # Workflow Progress
    # ------------------------------------------------------

    render_workflow_progress(dashboard)

    # ------------------------------------------------------
    # Pipeline Summary
    # ------------------------------------------------------

    render_pipeline_summary(dashboard)

    # ------------------------------------------------------
    # Recent Activity
    # ------------------------------------------------------

    render_recent_activity(dashboard)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()