#!/usr/bin/env python3
"""Validate a loaf YAML file for consistency and completeness."""

import sys
from pathlib import Path

import yaml

VALID_METHODS = ["dutch_oven", "steam_pan", "combo_cooker", "open_bake"]
VALID_BULK_STATES = ["underdone", "good", "peaked", "overfermented"]


def validate_loaf(data, filepath):
    """Run validation checks on loaf data."""
    errors = []
    warnings = []

    # Check required top-level fields
    required = ["loaf_number", "date", "ingredients", "process", "bake", "results"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Check bake method is valid
    if "bake" in data:
        method = data["bake"].get("method", "")
        if method and method not in VALID_METHODS:
            errors.append(f"Invalid bake method: '{method}'. Must be one of: {VALID_METHODS}")

    # Check bulk_end_state is valid
    if "process" in data:
        state = data["process"].get("bulk_end_state", "")
        if state and state not in VALID_BULK_STATES:
            errors.append(f"Invalid bulk_end_state: '{state}'. Must be one of: {VALID_BULK_STATES}")

    # Warn if quality_overall not filled
    if "results" in data:
        if data["results"].get("quality_overall", -1) == -1:
            warnings.append("quality_overall not filled - this is the most important field for analysis")

    # Check ingredient totals
    if "ingredients" in data:
        ing = data["ingredients"]
        total_flour = sum(v for k, v in ing.items() if k.startswith("flour_") and isinstance(v, (int, float)))
        if total_flour == 0:
            errors.append("No flour specified in ingredients")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate.py loaves/loaf-006.yaml")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    # Load YAML
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML syntax in {filepath}")
        print(str(e))
        sys.exit(1)

    # Validate
    errors, warnings = validate_loaf(data, filepath)

    # Report
    if errors:
        print(f"✗ Validation failed for {filepath}")
        for error in errors:
            print(f"  ERROR: {error}")
        if warnings:
            for warning in warnings:
                print(f"  WARNING: {warning}")
        sys.exit(1)
    elif warnings:
        print(f"⚠ Validation passed with warnings for {filepath}")
        for warning in warnings:
            print(f"  WARNING: {warning}")
    else:
        print(f"✓ Validation passed for {filepath}")


if __name__ == "__main__":
    main()
