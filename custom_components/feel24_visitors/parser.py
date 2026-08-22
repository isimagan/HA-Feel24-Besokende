"""Helpers for parsing Feel24 visitor data."""

from __future__ import annotations

import re

_VISITOR_COUNT_PATTERN = re.compile(
    r"<span\b[^>]*>\s*(\d+)\s*</span>\s*<br\s*/?>\s*treningsgjester\b",
    re.IGNORECASE | re.DOTALL,
)


def parse_visitor_count(html: str) -> int:
    """Extract the current visitor count from an iBooking visitors page."""
    match = _VISITOR_COUNT_PATTERN.search(html)
    if match is None:
        raise ValueError("Visitor count was not found in the iBooking response")

    return int(match.group(1))
