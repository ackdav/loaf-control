#!/usr/bin/env python3
"""Calculate derived fields for a loaf YAML file."""

import sys
import yaml
from pathlib import Path


def calculate_percentages(data):
    """Calculate baker's percentages from ingredient grams."""
    ing = data.get('ingredients', {})

    # Total flour - sum all fields starting with 'flour_'
    total_flour = sum(v for k, v in ing.items() if k.startswith('flour_') and isinstance(v, (int, float)))

    if total_flour == 0:
        print("Error: No flour specified in ingredients")
        return False

    # Calculate percentages
    water = ing.get('water', 0)
    levain = ing.get('levain', 0)
    salt = ing.get('salt', 0)

    data['hydration_pct'] = round(water / total_flour * 100, 1)
    data['inoculation_pct'] = round(levain / total_flour * 100, 1)
    data['salt_pct'] = round(salt / total_flour * 100, 2)

    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 calculate.py loaves/loaf-006.yaml")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    # Load YAML
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)

    # Calculate
    if not calculate_percentages(data):
        sys.exit(1)

    # Write back
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✓ Calculated percentages for {filepath}")
    print(f"  Hydration: {data['hydration_pct']}%")
    print(f"  Inoculation: {data['inoculation_pct']}%")
    print(f"  Salt: {data['salt_pct']}%")


if __name__ == '__main__':
    main()
