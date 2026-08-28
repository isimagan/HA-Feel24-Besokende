"""Tests for Feel24 visitor notification rules."""

from datetime import time
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "feel24_visitors"
    / "notification.py"
)
SPEC = importlib.util.spec_from_file_location("feel24_notification", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
NOTIFICATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NOTIFICATION)


class NotificationRulesTest(unittest.TestCase):
    """Verify threshold and time-window behavior."""

    def test_crossing_examples(self) -> None:
        """Only downward crossings from above the threshold trigger."""
        threshold = 2

        self.assertTrue(NOTIFICATION.crossed_threshold(3, 2, threshold))
        self.assertTrue(NOTIFICATION.crossed_threshold(3, 1, threshold))
        self.assertFalse(NOTIFICATION.crossed_threshold(2, 1, threshold))
        self.assertFalse(NOTIFICATION.crossed_threshold(1, 0, threshold))
        self.assertTrue(NOTIFICATION.crossed_threshold(5, 2, threshold))

    def test_sequence_rearms_only_above_threshold(self) -> None:
        """A sequence produces one alert until it rises above the threshold."""
        values = [5, 4, 2, 1, 0, 1, 3, 2]
        notifications = [
            current
            for previous, current in zip(values, values[1:])
            if NOTIFICATION.crossed_threshold(previous, current, 2)
        ]

        self.assertEqual(notifications, [2, 2])

    def test_invalid_values_are_not_numeric_counts(self) -> None:
        """Unknown-like and other non-numeric values never become zero."""
        for value in (None, "unknown", "unavailable", "2", True, float("nan")):
            with self.subTest(value=value):
                self.assertIsNone(NOTIFICATION.numeric_visitor_count(value))

        self.assertEqual(NOTIFICATION.numeric_visitor_count(0), 0)
        self.assertEqual(NOTIFICATION.numeric_visitor_count(2), 2)

    def test_notification_uses_actual_count_and_center(self) -> None:
        """The push text contains the actual count after a threshold jump."""
        self.assertEqual(
            NOTIFICATION.notification_message(1, "Feel24 Sandvika"),
            "Det er nå 1 besøkende på Feel24 Sandvika.",
        )
        self.assertEqual(
            NOTIFICATION.notification_message(2, "Feel24 Sandvika"),
            "Det er nå 2 besøkende på Feel24 Sandvika.",
        )

    def test_normal_time_window(self) -> None:
        """Normal daytime intervals include both boundaries."""
        self.assertTrue(
            NOTIFICATION.is_within_time_window(
                time(8, 0), "08:00:00", "22:00:00"
            )
        )
        self.assertTrue(
            NOTIFICATION.is_within_time_window(
                time(22, 0), "08:00:00", "22:00:00"
            )
        )
        self.assertFalse(
            NOTIFICATION.is_within_time_window(
                time(7, 59), "08:00:00", "22:00:00"
            )
        )

    def test_overnight_time_window(self) -> None:
        """Intervals crossing midnight include both sides of midnight."""
        self.assertTrue(
            NOTIFICATION.is_within_time_window(
                time(23, 0), "22:00:00", "02:00:00"
            )
        )
        self.assertTrue(
            NOTIFICATION.is_within_time_window(
                time(1, 30), "22:00:00", "02:00:00"
            )
        )
        self.assertFalse(
            NOTIFICATION.is_within_time_window(
                time(12, 0), "22:00:00", "02:00:00"
            )
        )

    def test_invalid_time_window_is_rejected(self) -> None:
        """Equal or malformed bounds are never interpreted as all day."""
        self.assertFalse(
            NOTIFICATION.is_within_time_window(
                time(12, 0), "08:00:00", "08:00:00"
            )
        )
        self.assertFalse(
            NOTIFICATION.is_within_time_window(time(12, 0), "bad", "22:00:00")
        )


if __name__ == "__main__":
    unittest.main()
