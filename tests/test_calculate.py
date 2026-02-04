"""Tests for baker's percentage calculations.

Validates hydration, inoculation, and salt percentages across various
flour combinations and edge cases.
"""

import pytest
from calculate import calculate_percentages


class TestBasicCalculations:
    """Core calculation logic with standard inputs."""

    def test_basic_percentages(self, basic_ingredients):
        """Verify correct baker's percentages for standard 70% hydration dough."""
        data = {"ingredients": basic_ingredients}

        assert calculate_percentages(data)
        assert data["hydration_pct"] == 70.0
        assert data["inoculation_pct"] == 20.0
        assert data["salt_pct"] == 2.0

    @pytest.mark.parametrize(
        "flour_amount,water_amount,expected_hydration",
        [
            (500, 360, 72.0),
            (500, 325, 65.0),
            (500, 400, 80.0),
            (333, 234, 70.3),  # Tests rounding precision
        ],
    )
    def test_hydration_variations(self, flour_amount, water_amount, expected_hydration):
        """Verify hydration calculations across common ratios."""
        data = {"ingredients": {"flour_dark": flour_amount, "water": water_amount, "salt": 10, "levain": 100}}

        assert calculate_percentages(data)
        assert data["hydration_pct"] == expected_hydration

    def test_multiple_flour_types_summed_correctly(self):
        """Ensure all flour_* fields contribute to total flour calculation."""
        data = {
            "ingredients": {
                "flour_half_white": 100,
                "flour_dark": 200,
                "flour_whole_grain": 150,
                "flour_rye": 50,
                "water": 350,
                "salt": 10,
                "levain": 100,
            }
        }

        assert calculate_percentages(data)
        # Total flour = 500, so 350/500 = 70%
        assert data["hydration_pct"] == 70.0
        assert data["inoculation_pct"] == 20.0
        assert data["salt_pct"] == 2.0


class TestEdgeCases:
    """Boundary conditions and error handling."""

    @pytest.mark.parametrize(
        "ingredients",
        [
            {"water": 350, "salt": 10, "levain": 100},  # No flour fields
            {"flour_dark": 0, "water": 350},  # Zero flour
            {"flour_dark": 0, "flour_rye": 0},  # All flours zero
        ],
    )
    def test_no_flour_returns_false(self, ingredients):
        """Reject calculations when total flour is zero or missing."""
        data = {"ingredients": ingredients}
        assert calculate_percentages(data) is False

    def test_missing_ingredient_fields_default_to_zero(self):
        """Handle missing water/salt/levain gracefully (treats as 0g)."""
        data = {"ingredients": {"flour_dark": 500}}

        assert calculate_percentages(data)
        assert data["hydration_pct"] == 0.0
        assert data["inoculation_pct"] == 0.0
        assert data["salt_pct"] == 0.0

    def test_non_flour_fields_ignored_in_total(self):
        """Verify only flour_* prefixed fields count toward flour total."""
        data = {
            "ingredients": {
                "flour_dark": 400,
                "flour_rye": 100,
                "water": 350,
                "levain": 100,
                "random_additive": 999,
                "sourdough_starter": 50,  # Not flour_* prefix
            }
        }

        assert calculate_percentages(data)
        # Should only count 400 + 100 = 500 flour
        assert data["hydration_pct"] == 70.0

    @pytest.mark.parametrize(
        "flour_type",
        [
            "flour_half_white",
            "flour_dark",
            "flour_whole_grain",
            "flour_rye",
            "flour_spelt",  # Not in current schema but should work
        ],
    )
    def test_any_flour_prefix_counted(self, flour_type):
        """Support arbitrary flour_* field names for extensibility."""
        data = {"ingredients": {flour_type: 500, "water": 350, "salt": 10, "levain": 100}}

        assert calculate_percentages(data)
        assert data["hydration_pct"] == 70.0


class TestNumericPrecision:
    """Floating point and rounding behavior."""

    def test_handles_float_values(self):
        """Accept decimal measurements (e.g., 10.5g salt)."""
        data = {"ingredients": {"flour_dark": 500.5, "water": 350.3, "salt": 10.2, "levain": 100.1}}

        assert calculate_percentages(data)
        assert isinstance(data["hydration_pct"], float)
        assert isinstance(data["inoculation_pct"], float)
        assert isinstance(data["salt_pct"], float)

    def test_rounding_precision_matches_spec(self):
        """Verify hydration/inoculation round to 1 decimal, salt to 2 decimals."""
        data = {"ingredients": {"flour_dark": 333, "water": 234, "salt": 7, "levain": 66}}

        assert calculate_percentages(data)
        # Hydration: 234/333 = 70.27027... → 70.3 (1 decimal)
        assert data["hydration_pct"] == 70.3
        # Inoculation: 66/333 = 19.81981... → 19.8 (1 decimal)
        assert data["inoculation_pct"] == 19.8
        # Salt: 7/333 = 2.102102... → 2.1 (2 decimals, but trailing zero dropped)
        assert data["salt_pct"] == 2.1

    def test_very_high_inoculation_percentage(self):
        """Handle edge case of levain exceeding flour weight (100%+ inoculation)."""
        data = {"ingredients": {"flour_dark": 100, "water": 100, "levain": 150, "salt": 2}}

        assert calculate_percentages(data)
        assert data["inoculation_pct"] == 150.0
        assert data["hydration_pct"] == 100.0
