"""
2_Dataset.py

Purpose:
    Dataset management page.

Author:
    Shahid

Project:
    ML Studio
"""

from src.services.dataset_service import DatasetService

from src.ui.components.dataset import (
    render_upload_section,
    render_dataset_summary,
    render_dataset_preview,
    render_column_summary,
)

from src.ui.layouts.page_layout import (
    PageConfig,
    render_page_layout,
)

from src.core.app_initializer import initialize_page


initialize_page()


def main() -> None:
    """
    Render Dataset page.
    """

    render_page_layout(
        PageConfig(
            title="Dataset",
            description="Upload and inspect your dataset.",
            icon="📂",
        )
    )

    dataset = DatasetService.get_dataset_data()

    render_upload_section(dataset)

    render_dataset_summary(dataset)

    render_dataset_preview(dataset)

    render_column_summary(dataset)


if __name__ == "__main__":
    main()