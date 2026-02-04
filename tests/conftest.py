"""Shared test fixtures and configuration."""

import sys
from pathlib import Path

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture
def valid_loaf_data():
    """Minimal valid loaf data structure."""
    return {
        "loaf_number": 1,
        "date": "2026-02-04",
        "ingredients": {"flour_dark": 500, "water": 350, "salt": 10, "levain": 100},
        "process": {"bulk_end_state": "good"},
        "bake": {"method": "dutch_oven"},
        "results": {"quality_overall": 3},
    }


@pytest.fixture
def basic_ingredients():
    """Standard ingredient ratios for testing calculations."""
    return {"flour_dark": 400, "flour_rye": 100, "water": 350, "salt": 10, "levain": 100}
