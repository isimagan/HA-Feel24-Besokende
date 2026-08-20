"""Tests for Feel24 gym validation."""

import importlib.util
from pathlib import Path
import unittest

GYMS_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "feel24_visitors"
    / "gyms.py"
)
SPEC = importlib.util.spec_from_file_location("feel24_gyms", GYMS_PATH)
assert SPEC and SPEC.loader
GYMS_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GYMS_MODULE)

GYMS = GYMS_MODULE.GYMS
resolve_gym = GYMS_MODULE.resolve_gym
select_effective_gym = GYMS_MODULE.select_effective_gym


class GymValidationTests(unittest.TestCase):
    """Test Feel24 gym validation."""

    def test_gym_list_is_unique(self) -> None:
        """The configured gym list must not contain duplicates."""
        self.assertEqual(len(GYMS), len(set(GYMS)))

    def test_resolve_exact_gym(self) -> None:
        """An exact gym name resolves to itself."""
        self.assertEqual(
            resolve_gym("Feel24 Tromsø Fagereng"), "Feel24 Tromsø Fagereng"
        )

    def test_resolve_normalizes_case_and_whitespace(self) -> None:
        """Case and repeated whitespace do not make a valid gym invalid."""
        self.assertEqual(
            resolve_gym("  feel24   tromsø fagereng "),
            "Feel24 Tromsø Fagereng",
        )

    def test_resolve_empty_gym(self) -> None:
        """The gym field is optional."""
        self.assertEqual(resolve_gym(""), "")
        self.assertEqual(resolve_gym(None), "")

    def test_resolve_unknown_gym(self) -> None:
        """An unknown gym does not resolve."""
        self.assertIsNone(resolve_gym("Feel24 Atlantis"))

    def test_fixed_gym_takes_precedence(self) -> None:
        """A gym chosen in the config flow cannot be overridden at runtime."""
        self.assertEqual(
            select_effective_gym("Feel24 Billingstad", "Feel24 Tromsø Fagereng"),
            "Feel24 Billingstad",
        )

    def test_runtime_gym_is_used_when_config_is_empty(self) -> None:
        """The runtime selector controls the sensor when no gym is fixed."""
        self.assertEqual(
            select_effective_gym("", "Feel24 Tromsø Fagereng"),
            "Feel24 Tromsø Fagereng",
        )


if __name__ == "__main__":
    unittest.main()
