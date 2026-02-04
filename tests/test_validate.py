"""Tests for YAML validation logic.

Ensures loaf data meets schema requirements and catches common errors
before they corrupt the dataset.
"""

from pathlib import Path

import pytest
from validate import VALID_BULK_STATES, VALID_METHODS, validate_loaf


class TestValidationSuccess:
    """Cases that should pass validation."""

    def test_minimal_valid_loaf(self, valid_loaf_data):
        """Verify baseline valid loaf structure passes all checks."""
        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))

        assert len(errors) == 0
        assert len(warnings) == 0

    @pytest.mark.parametrize("method", VALID_METHODS)
    def test_all_bake_methods_accepted(self, valid_loaf_data, method):
        """Ensure every documented bake method passes validation."""
        valid_loaf_data["bake"]["method"] = method

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) == 0

    @pytest.mark.parametrize("state", VALID_BULK_STATES)
    def test_all_bulk_states_accepted(self, valid_loaf_data, state):
        """Ensure every documented bulk fermentation state passes."""
        valid_loaf_data["process"]["bulk_end_state"] = state

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) == 0

    @pytest.mark.parametrize(
        "method,state",
        [
            ("", ""),  # Empty strings (sentinel for "not recorded")
            (None, None),  # Missing keys entirely
        ],
    )
    def test_optional_enums_allow_empty(self, valid_loaf_data, method, state):
        """Don't enforce enums when user hasn't filled them yet."""
        if method is not None:
            valid_loaf_data["bake"]["method"] = method
        else:
            del valid_loaf_data["bake"]["method"]

        if state is not None:
            valid_loaf_data["process"]["bulk_end_state"] = state
        else:
            del valid_loaf_data["process"]["bulk_end_state"]

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) == 0


class TestValidationErrors:
    """Cases that should fail validation."""

    @pytest.mark.parametrize("missing_field", ["loaf_number", "date", "ingredients", "process", "bake", "results"])
    def test_required_fields_enforced(self, valid_loaf_data, missing_field):
        """Reject loaves missing critical top-level fields."""
        del valid_loaf_data[missing_field]

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) > 0
        assert any(missing_field in e for e in errors)

    @pytest.mark.parametrize(
        "invalid_method",
        [
            "microwave",
            "air_fryer",
            "DUTCH_OVEN",  # Case sensitive
            "dutch-oven",  # Wrong delimiter
        ],
    )
    def test_invalid_bake_method_rejected(self, valid_loaf_data, invalid_method):
        """Catch typos and unsupported baking methods."""
        valid_loaf_data["bake"]["method"] = invalid_method

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) > 0
        assert any("bake method" in e.lower() for e in errors)

    @pytest.mark.parametrize(
        "invalid_state",
        [
            "burnt",
            "perfect",
            "GOOD",  # Case sensitive
            "under-done",  # Wrong delimiter
        ],
    )
    def test_invalid_bulk_state_rejected(self, valid_loaf_data, invalid_state):
        """Catch typos in fermentation state tracking."""
        valid_loaf_data["process"]["bulk_end_state"] = invalid_state

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) > 0
        assert any("bulk_end_state" in e for e in errors)

    @pytest.mark.parametrize(
        "ingredients",
        [
            {},  # Empty ingredients
            {"water": 350, "salt": 10},  # No flour at all
            {"flour_dark": 0, "flour_rye": 0, "water": 350},  # All flour zero
        ],
    )
    def test_flour_requirement_enforced(self, valid_loaf_data, ingredients):
        """Prevent nonsensical bakes with no flour."""
        valid_loaf_data["ingredients"] = ingredients

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) > 0
        assert any("flour" in e.lower() for e in errors)


class TestValidationWarnings:
    """Cases that pass but should warn user."""

    @pytest.mark.parametrize("quality_value", [-1, None])
    def test_missing_quality_generates_warning(self, valid_loaf_data, quality_value):
        """Remind user to rate quality since it's critical for analysis."""
        if quality_value is None:
            del valid_loaf_data["results"]["quality_overall"]
        else:
            valid_loaf_data["results"]["quality_overall"] = quality_value

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) == 0
        assert len(warnings) > 0
        assert any("quality_overall" in w for w in warnings)

    def test_quality_filled_suppresses_warning(self, valid_loaf_data):
        """Don't nag user if they've already rated the loaf."""
        valid_loaf_data["results"]["quality_overall"] = 4

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(warnings) == 0


class TestErrorAccumulation:
    """Verify multiple issues are caught in one pass."""

    def test_multiple_errors_reported_together(self):
        """Don't stop at first error - show all problems at once."""
        data = {
            "loaf_number": 1,
            # Missing: date, ingredients, process, bake, results
            "bake": {"method": "invalid_method"},
        }

        errors, warnings = validate_loaf(data, Path("test.yaml"))
        # Should have errors for missing fields + invalid method
        assert len(errors) >= 4

    def test_errors_and_warnings_coexist(self, valid_loaf_data):
        """Show both critical errors and advisory warnings."""
        valid_loaf_data["bake"]["method"] = "microwave"  # Error
        valid_loaf_data["results"]["quality_overall"] = -1  # Warning

        errors, warnings = validate_loaf(valid_loaf_data, Path("test.yaml"))
        assert len(errors) > 0
        assert len(warnings) > 0
