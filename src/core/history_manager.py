"""
history_manager.py

Purpose:
    Stores user activity history for ML Studio.

Author:
    Shahid

Project:
    ML Studio
"""

from datetime import datetime
from typing import Any

from src.core.session_manager import SessionManager


class HistoryManager:
    """
    Manages user activity history.
    """

    HISTORY_KEY = "history"

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize history.
        """
        if SessionManager.get(cls.HISTORY_KEY) is None:
            SessionManager.set(cls.HISTORY_KEY, [])

    @classmethod
    def add_event(
        cls,
        action: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Add an event to history.
        """

        history = SessionManager.get(cls.HISTORY_KEY)

        history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": action,
                "details": details or {},
            }
        )

        SessionManager.set(cls.HISTORY_KEY, history)

    @classmethod
    def get_history(cls) -> list:
        """
        Return the complete history.
        """
        return SessionManager.get(cls.HISTORY_KEY)

    @classmethod
    def clear(cls) -> None:
        """
        Remove all history entries.
        """
        SessionManager.set(cls.HISTORY_KEY, [])

    @classmethod
    def get_latest_event(cls) -> dict | None:
        """
        Return the latest history event.
        """
        history = SessionManager.get(cls.HISTORY_KEY)

        if history:
            return history[-1]

        return None