"""Pure helpers for Feel24 visitor notifications."""

from __future__ import annotations

from datetime import time
import math
from numbers import Real


def numeric_visitor_count(value: object) -> int | float | None:
    """Return a valid numeric visitor count, excluding booleans and invalid data."""
    if isinstance(value, bool) or not isinstance(value, Real):
        return None

    numeric_value = float(value)
    if not math.isfinite(numeric_value) or numeric_value < 0:
        return None
    return int(numeric_value) if numeric_value.is_integer() else numeric_value


def crossed_threshold(
    previous: int | float | None,
    current: int | float | None,
    threshold: int | float,
) -> bool:
    """Return whether the count crossed from above to at or below a threshold."""
    return (
        previous is not None
        and current is not None
        and previous > threshold
        and current <= threshold
    )


def is_within_time_window(
    current: time,
    start: str,
    end: str,
) -> bool:
    """Return whether a time is in a normal or overnight interval, inclusively."""
    try:
        start_time = time.fromisoformat(start)
        end_time = time.fromisoformat(end)
    except (TypeError, ValueError):
        return False

    current_time = current.replace(tzinfo=None)
    if start_time == end_time:
        return False
    if start_time < end_time:
        return start_time <= current_time <= end_time
    return current_time >= start_time or current_time <= end_time


def notification_message(count: int | float, center_name: str) -> str:
    """Build a concise Norwegian visitor notification message."""
    displayed_count = int(count) if float(count).is_integer() else count
    return f"Det er nå {displayed_count} besøkende på {center_name}."
